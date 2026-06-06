import fs from "fs";
import path from "path";
import postcss from "postcss";
import eleventyAutoCacheBuster from "eleventy-auto-cache-buster";
import tailwindcss from "@tailwindcss/postcss";

export default function (eleventyConfig) {
  //   eleventyConfig.addPlugin(eleventyAutoCacheBuster, {
  //     extensions: ["css","js","json"],
  // });

  // 1. Static Asset Passthrough
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/data");
  eleventyConfig.addPassthroughCopy("src/_headers");

  // 2. Tailwind v4 + PostCSS Build Hook
  eleventyConfig.on("eleventy.before", async () => {
    const inputPath = path.resolve("./src/assets/css/main.css");
    const outputPath = "./_site/assets/css/style.css";

    try {
      const cssContent = fs.readFileSync(inputPath, "utf8");
      const outputDir = path.dirname(outputPath);

      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }

      const result = await postcss([tailwindcss()]).process(cssContent, {
        from: inputPath,
        to: outputPath,
      });

      fs.writeFileSync(outputPath, result.css);
      console.log(`[Tailwind] Build successful: ${outputPath}`);
    } catch (err) {
      console.error("[Tailwind] Build failed:", err);
    }
  });

eleventyConfig.addCollection("orvChapters", function (collectionApi) {
  return collectionApi
    .getFilteredByGlob("src/story/orv/**/*.html")
    .sort((a, b) => (a.data.index || 0) - (b.data.index || 0));
});

  return {
    dir: {
      input: "src",
      output: "_site",
    },
  };
}
