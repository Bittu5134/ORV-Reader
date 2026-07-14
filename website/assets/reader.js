function changeGiscusTheme(theme) {
    // const scriptId = 'giscus-script';
    // const existingScript = document.getElementById(scriptId);
    // let theme = window.theme;


    if (theme === "dark") {
        theme = "dark";
    } else if (theme === "light") {
        theme = "light";
    } else if (theme === "sepia") {
        theme = "gruvbox_light";
    } else if (theme === "pastel") {
        theme = "light";
    } else if (theme === "midnight") {
        theme = "transparent_dark";
    } else if (theme === "forest") {
        theme = "light";
    } else if (theme === "paper") {
        theme = "light";
    } else if (theme === "lavender") {
        theme = "catppuccin_latte";
    } else if (theme === "dark-sepia") {
        theme = "gruvbox_dark";
    } else if (theme === "dark-pastel") {
        theme = "catppuccin_frappe";
    } else if (theme === "dark-forest") {
        theme = "transparent_dark";
    } else if (theme === "dark-paper") {
        theme = "transparent_dark";
    } else if (theme === "dark-lavender") {
        theme = "catppuccin_mocha";
    }

    function sendMessage(message) {
        const iframe = document.querySelector('iframe.giscus-frame');
        if (!iframe) return;
        iframe.contentWindow.postMessage({ giscus: message }, 'https://giscus.app');
    }

    sendMessage({
        setConfig: {
            theme: theme
        }
    });

    // if (existingScript) {
    //     existingScript.remove();
    //     console.log('Giscus script removed.');
    // }

    // document.getElementById("comments").innerHTML = ""

    // const script = document.createElement('script');
    // script.id = scriptId;
    // script.src = 'https://giscus.app/client.js';
    // script.setAttribute('data-repo', 'Bittu5134/ORV-Reader');
    // script.setAttribute('data-repo-id', 'R_kgDOOHNFOQ');
    // script.setAttribute('data-category', 'General');
    // script.setAttribute('data-category-id', 'DIC_kwDOOHNFOc4CoREL');
    // script.setAttribute('data-mapping', 'title');
    // script.setAttribute('data-strict', '1');
    // script.setAttribute('data-reactions-enabled', '1');
    // script.setAttribute('data-emit-metadata', '0');
    // script.setAttribute('data-input-position', 'top');
    // script.setAttribute('data-theme', theme);
    // script.setAttribute('data-lang', 'en');
    // script.setAttribute('crossorigin', 'anonymous');
    // script.async = true;

    // document.body.appendChild(script);
    console.log('Giscus script added.');

}


setInterval(() => {
    changeGiscusTheme(window.theme)
}, 2000)


setTimeout(() => {
    const scriptElement = document.getElementById('main-script');
    let index = scriptElement.dataset.index;
    let type = scriptElement.dataset.type;
    localStorage.setItem("lastread", String(index))
    localStorage.setItem("lasttype", String(type))
}, 10000);

function classChangeTheme(elementClass, elemetTheme) {
    let element = document.getElementsByClassName(elementClass)

    Array.from(element).forEach(item => {
        item.classList.remove("theme1")
        item.classList.remove("theme2")
        item.classList.remove("theme3")
        item.classList.remove("theme4")
        item.classList.remove("theme5")
        item.classList.remove("theme6")
        item.classList.add(elemetTheme)
    });
}



function loadSettingsFromLocalStorage() {
    try {
        let settings = JSON.parse(localStorage.getItem('settings1'));

        if (!settings) return null;

        if (settings.theme) {
            document.getElementById('set-theme').value = settings.theme;
        }
        if (settings.font) {
            document.getElementById('set-font').value = settings.font;
        }
        if (settings.fontSize) {
            if (settings.fontSize == 52) { settings.fontSize = 51; }
            document.getElementById('set-font-size').value = settings.fontSize;
        }
        if (settings.fontWeight) {
            document.getElementById('set-font-weight').value = settings.fontWeight;
        }
        if (settings.lineHeight) {
            if (settings.lineHeight == 32) { settings.lineHeight = 49; } // legacy code
            document.getElementById('set-line-height').value = settings.lineHeight;
        }
        if (settings.richTextToggle !== undefined) {
            document.getElementById('set-rich-text-toggle').checked = settings.richTextToggle;
        }
        if (settings.systemMsgStyle) {
            document.getElementById('set-rich-system-msg').value = settings.systemMsgStyle;
        }
        if (settings.systemWindowStyle) {
            document.getElementById('set-rich-system-window').value = settings.systemWindowStyle;
        }
        if (settings.constSpeechStyle) {
            document.getElementById('set-rich-const').value = settings.constSpeechStyle;
        }
        if (settings.outerSpeechStyle) {
            document.getElementById('set-rich-outer').value = settings.outerSpeechStyle;
        }
        if (settings.quoteStyle) {
            document.getElementById('set-rich-quote').value = settings.quoteStyle;
        }
        if (settings.noticeStyle) {
            document.getElementById('set-rich-notice').value = settings.noticeStyle;
        }
        if (settings.genericBoxStyle) {
            document.getElementById('set-rich-box').value = settings.genericBoxStyle;
        }



        // Return the settings object if needed.
        return settings;

    } catch (error) {
        console.error('Error loading settings from local storage:', error);
        return {};
    }
}

loadSettingsFromLocalStorage();


window.theme = "dark"

document.addEventListener('DOMContentLoaded', function () {



    // this is for settings
    const settingsForm = document.getElementById('settings-form');

    function applySettings() {
        let root = document.documentElement;
        let theme = document.getElementById('set-theme').value;
        let font = document.getElementById('set-font').value;
        let fontSize = document.getElementById('set-font-size').value;
        let fontWeight = document.getElementById('set-font-weight').value;
        let lineHeight = document.getElementById('set-line-height').value;
        let richTextToggle = document.getElementById('set-rich-text-toggle').checked;
        let systemMsgStyle = document.getElementById('set-rich-system-msg').value;
        let systemWindowStyle = document.getElementById('set-rich-system-window').value;
        let constSpeechStyle = document.getElementById('set-rich-const').value;
        let outerSpeechStyle = document.getElementById('set-rich-outer').value;
        let quoteStyle = document.getElementById('set-rich-quote').value;
        let noticeStyle = document.getElementById('set-rich-notice').value;
        let genericBoxStyle = document.getElementById('set-rich-box').value;

        if (fontSize < 30) { fontSize = 30; }
        if (fontSize > 100) { fontSize = 100; }
        fontSize = fontSize / 3;
        fontSize = fontSize + "px";

        if (lineHeight > 100) { lineHeight = 100; }
        if (lineHeight < 1) { lineHeight = 1; }
        lineHeight = lineHeight / 30.625
        root.style.setProperty('--line-space', lineHeight + "rem")

        window.theme = theme;

        changeGiscusTheme(theme)

        if (theme === "dark") {
            root.style.setProperty("--body-background", "#14151b");
            root.style.setProperty("--primary", "#1f2129");
            root.style.setProperty("--nav", "#18191f");
            root.style.setProperty("--text-primary", "#b6bccc");
            root.style.setProperty("--text-secondary", "#c6cee2");
            root.style.setProperty("--icons-color", "");

        } else if (theme === "light") {
            root.style.setProperty("--body-background", "#ffffff");
            root.style.setProperty("--primary", "#f0f0f0");
            root.style.setProperty("--nav", "#d0d0d0");
            root.style.setProperty("--text-primary", "#000000");
            root.style.setProperty("--text-secondary", "#333333");
            root.style.setProperty("--icons-color", "brightness(40%)");

        } else if (theme === "sepia") {
            root.style.setProperty("--body-background", "#cab793");
            root.style.setProperty("--primary", "#f5deb3");
            root.style.setProperty("--nav", "#ac9b7c");
            root.style.setProperty("--text-primary", "#000000");
            root.style.setProperty("--text-secondary", "#000000");
            root.style.setProperty("--icons-color", "");
            root.style.setProperty("--icons-color", "brightness(40%)");

        } else if (theme === "pastel") {
            root.style.setProperty("--body-background", "#f9f5f6");
            root.style.setProperty("--primary", "#f0e6ef");
            root.style.setProperty("--nav", "#e3c2d9");
            root.style.setProperty("--text-primary", "#4a3b4c");
            root.style.setProperty("--text-secondary", "#635066");
            root.style.setProperty("--icons-color", "brightness(40%)");
        } else if (theme === "midnight") {
            root.style.setProperty("--body-background", "#000");
            root.style.setProperty("--primary", "#000");
            root.style.setProperty("--nav", "#0e0e18");
            root.style.setProperty("--text-primary", "#c0c8d0");
            root.style.setProperty("--text-secondary", "#a8b0b8");
            root.style.setProperty("--icons-color", "brightness(100)");

        } else if (theme === "forest") {
            root.style.setProperty("--body-background", "#e8f5e9");
            root.style.setProperty("--primary", "#c8e6c9");
            root.style.setProperty("--nav", "#a5d6a7");
            root.style.setProperty("--text-primary", "#2e7d32");
            root.style.setProperty("--text-secondary", "#388e3c");
            root.style.setProperty("--icons-color", "brightness(40%)");

        } else if (theme === "paper") {
            root.style.setProperty("--body-background", "#f8f5f0");
            root.style.setProperty("--primary", "#f5f0e8");
            root.style.setProperty("--nav", "#e8e0d8");
            root.style.setProperty("--text-primary", "#333333");
            root.style.setProperty("--text-secondary", "#444444");
            root.style.setProperty("--icons-color", "brightness(40%)");

        } else if (theme === "lavender") {
            root.style.setProperty("--body-background", "#f3efff");
            root.style.setProperty("--primary", "#ede7f6");
            root.style.setProperty("--nav", "#ded5e8");
            root.style.setProperty("--text-primary", "#4527a0");
            root.style.setProperty("--text-secondary", "#512da8");
            root.style.setProperty("--icons-color", "brightness(40%)");

        } else if (theme === "dark-sepia") {
            root.style.setProperty("--body-background", "#2a241e");
            root.style.setProperty("--primary", "#322c26");
            root.style.setProperty("--nav", "#2e2822");
            root.style.setProperty("--text-primary", "#d2c8bc");
            root.style.setProperty("--text-secondary", "#c0b6aa");
            root.style.setProperty("--icons-color", "brightness(100%)");

        } else if (theme === "dark-pastel") {
            root.style.setProperty("--body-background", "#1e1b1e");
            root.style.setProperty("--primary", "#28252a");
            root.style.setProperty("--nav", "#252227");
            root.style.setProperty("--text-primary", "#d1c2d3");
            root.style.setProperty("--text-secondary", "#b9a9bc");
            root.style.setProperty("--icons-color", "brightness(100%)");

        } else if (theme === "dark-forest") {
            root.style.setProperty("--body-background", "#121813");
            root.style.setProperty("--primary", "#1a221b");
            root.style.setProperty("--nav", "#171f18");
            root.style.setProperty("--text-primary", "#b8d2b9");
            root.style.setProperty("--text-secondary", "#a6c0a7");
            root.style.setProperty("--icons-color", "brightness(100%)");

        } else if (theme === "dark-paper") {
            root.style.setProperty("--body-background", "#1c1b1a");
            root.style.setProperty("--primary", "#242322");
            root.style.setProperty("--nav", "#222120");
            root.style.setProperty("--text-primary", "#d4d3d2");
            root.style.setProperty("--text-secondary", "#c2c1c0");
            root.style.setProperty("--icons-color", "brightness(100%)");

        } else if (theme === "dark-lavender") {
            root.style.setProperty("--body-background", "#1c1920");
            root.style.setProperty("--primary", "#24202a");
            root.style.setProperty("--nav", "#221e26");
            root.style.setProperty("--text-primary", "#d2c9e0");
            root.style.setProperty("--text-secondary", "#c0b7d0");
            root.style.setProperty("--icons-color", "brightness(100%)");

        }


        document.body.className = theme;

        root.style.setProperty('--default-font', font);
        document.body.style.fontSize = fontSize;
        document.body.style.fontWeight = fontWeight

        const settings = {
            theme: document.getElementById('set-theme').value,
            font: document.getElementById('set-font').value,
            fontSize: document.getElementById('set-font-size').value,
            fontWeight: document.getElementById('set-font-weight').value,
            lineHeight: document.getElementById('set-line-height').value,
            richTextToggle: document.getElementById('set-rich-text-toggle').checked,
            systemMsgStyle: document.getElementById('set-rich-system-msg').value,
            systemWindowStyle: document.getElementById('set-rich-system-window').value,
            constSpeechStyle: document.getElementById('set-rich-const').value,
            outerSpeechStyle: document.getElementById('set-rich-outer').value,
            quoteStyle: document.getElementById('set-rich-quote').value,
            noticeStyle: document.getElementById('set-rich-notice').value,
            genericBoxStyle: document.getElementById('set-rich-box').value,
        };



        try {
            localStorage.setItem('settings1', JSON.stringify(settings));
            console.log('Settings saved to local storage.');
        } catch (error) {
            console.error('Error saving settings to local storage:', error);
        }



        if (richTextToggle) {
            document.getElementById('set-rich-system-msg').disabled = false;
            document.getElementById('set-rich-system-window').disabled = false;
            document.getElementById('set-rich-const').disabled = false;
            document.getElementById('set-rich-outer').disabled = false;
            document.getElementById('set-rich-quote').disabled = false;
            document.getElementById('set-rich-notice').disabled = false;
            document.getElementById('set-rich-box').disabled = false;

        } else {
            document.getElementById('set-rich-system-msg').disabled = true;
            document.getElementById('set-rich-system-window').disabled = true;
            document.getElementById('set-rich-const').disabled = true;
            document.getElementById('set-rich-outer').disabled = true;
            document.getElementById('set-rich-quote').disabled = true;
            document.getElementById('set-rich-notice').disabled = true;
            document.getElementById('set-rich-box').disabled = true;

            richTextToggle = "theme1"
            systemMsgStyle = "theme1"
            systemWindowStyle = "theme1"
            constSpeechStyle = "theme1"
            outerSpeechStyle = "theme1"
            quoteStyle = "theme1"
            noticeStyle = "theme1"
            genericBoxStyle = "theme1"

            console.log("Rich text features disabled");
        }

        classChangeTheme("orv_system", systemMsgStyle)
        classChangeTheme("orv_window", systemWindowStyle)
        classChangeTheme("orv_constellation", constSpeechStyle)
        classChangeTheme("orv_outergod", outerSpeechStyle)
        classChangeTheme("orv_quote", quoteStyle)
        classChangeTheme("orv_notice", noticeStyle)
        classChangeTheme("orv_box", genericBoxStyle)
    }

    applySettings();
    window.applySettings = applySettings;


    settingsForm.addEventListener('change', function (event) {
        applySettings();
    });

    document.getElementById('set-font-size').addEventListener('input', function (event) {
        applySettings();
    });
    document.getElementById('set-font-weight').addEventListener('input', function (event) {
        applySettings();
    });
    document.getElementById('set-line-height').addEventListener('input', function (event) {
        applySettings();
    });

    settingsForm.addEventListener('reset', function (event) {
        setTimeout(applySettings, 0);
    });

    const scriptElement = document.getElementById('main-script');
    if (!scriptElement) {
        console.error("Element #main-script not found.");
        return;
    }
    const index = scriptElement.dataset.index;
    const type = scriptElement.dataset.type;
    const scrollKey = `scrollY_${type}_${index}`;

    try {
        const savedScroll = localStorage.getItem(scrollKey);
        if (savedScroll !== null) {
            window.scrollTo(0, parseInt(savedScroll, 10));
        }
    } catch (e) {
        console.error('Error restoring scroll:', e);
    }

    function saveScrollPosition() {
        try {
            localStorage.setItem(scrollKey, window.scrollY);

            const SCROLL_HISTORY_KEY = `scroll_history_${type}`;
            const MAX_HISTORY_SIZE = 5;

            let history = JSON.parse(localStorage.getItem(SCROLL_HISTORY_KEY)) || [];

            history = history.filter(key => key !== scrollKey);

            history.unshift(scrollKey);

            while (history.length > MAX_HISTORY_SIZE) {
                const oldestKey = history.pop();
                localStorage.removeItem(oldestKey);
            }

            localStorage.setItem(SCROLL_HISTORY_KEY, JSON.stringify(history));
        } catch (e) {
            console.error('Error saving scroll:', e);
        }
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    window.addEventListener('scroll', debounce(saveScrollPosition, 500));
    window.addEventListener('beforeunload', saveScrollPosition);
});



let chFetchStatus = false;
const ChapterList = [];

function addAllChapters() {

    // load data tags

    const scriptElement = document.getElementById('main-script');
    let titles_url = scriptElement.dataset.titles;

    if (!chFetchStatus) {
        fetch(titles_url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                ChapterList.push(...data);
                console.log("Chapters loaded:", ChapterList);
                chFetchStatus = true;

            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            })
            .then(() => {
                let chapterSearch = document.getElementById("chapter-search-reasult");
                let chapterTitle = document.getElementsByClassName("orv_title")[0].textContent.trim();
                let chapterID = "";
                let chSearchresult = [];

                ChapterList.forEach(chapter => {
                    if (chapterTitle === chapter.title) {
                        chapterID = "current-chapter";
                        chapter.index = "";
                    }
                    // chSearchresult.push(`<div class="chapter_item" id="${chapterID}"><p><a href="#${chapter.index}">${chapter.title}</a></p></div>`);
                    chSearchresult.push(`<div class="chapter_item" id="${chapterID}"><a href="./ch_${chapter.index + 1}"><p>${chapter.title}</p></a></div>`);
                    chapterID = "";
                });

                chapterSearch.innerHTML = chSearchresult.join("");
                document.getElementById("current-chapter").scrollIntoView({ behavior: "smooth", block: "center" });
            });
    }
}

function openChapters() {
    addAllChapters()
    document.getElementById('chapters').style.display = 'block'
}



function findChapter() {
    let chapter = document.getElementById("find-chapter").value.trim();
    let chapterSearch = document.getElementById("chapter-search-reasult")
    chapterSearch.innerHTML = ""
    let chSearchresult = []

    for (let i = 0; i < ChapterList.length; i++) {
        let displayTitle = String(ChapterList[i].title)
        let title = displayTitle.toLowerCase();
        let chSearchindex = title.indexOf(chapter.toLowerCase());
        let index = ChapterList[i].index;
        if (chSearchindex !== -1) {
            chSearchresult.push(`<div class="chapter_item"><a href="./ch_${index + 1}"><p>${displayTitle}</p></a></div>`);
        }

    }
    chapterSearch.innerHTML = chSearchresult.join("");

    if (chSearchresult.length === 0) {
        chapterSearch.innerHTML = `<div class="chapter_item"><p>Chapter not found</p></div>`;
    }
}



let wakeLock = null;

async function requestWakeLock() {
  try {
    wakeLock = await navigator.wakeLock.request('screen');
    console.log('Wake Lock is active!');

    wakeLock.addEventListener('release', () => {
      console.log('Wake Lock was released.');
      wakeLock = null;
    });
  } catch (err) {
    console.error(`Failed to acquire wake lock: ${err}`);
  }
}

async function releaseWakeLock() {
  if (wakeLock) {
    await wakeLock.release();
    wakeLock = null;
    console.log('Wake Lock released.');
  }
}

// Request wake lock when the page loads
window.addEventListener('load', requestWakeLock);

// Request wake lock when the page is navigated back to
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    requestWakeLock()
  }
});

// Release wake lock when the page is unloaded (navigated away from or closed)
window.addEventListener('beforeunload', releaseWakeLock);

// Optional: Release wake lock on history navigation
window.addEventListener('popstate', releaseWakeLock);

// Giscus error detection & auth redirection logic for rate limiting
(function() {
    let giscusLoaded = false;
    let bannerTriggered = false;

    function showGiscusAuthBanner() {
        if (bannerTriggered) return;
        bannerTriggered = true;

        const commentsDiv = document.getElementById('comments');
        if (!commentsDiv) return;

        // Check if banner already exists
        if (document.getElementById('giscus-auth-banner')) return;

        const oldScript = document.getElementById('giscus-script');
        const discussionId = oldScript ? oldScript.getAttribute('data-term') : null;
        const githubDiscussionUrl = (discussionId && !isNaN(discussionId))
            ? `https://github.com/Bittu5134/ORV-Reader/discussions/${discussionId}`
            : 'https://github.com/Bittu5134/ORV-Reader/discussions';

        const banner = document.createElement('div');
        banner.id = 'giscus-auth-banner';
        banner.className = 'theme1'; // matches site styles
        banner.style.margin = '20px auto';
        banner.style.padding = '20px';
        banner.style.backgroundColor = 'var(--primary)';
        banner.style.border = '1px solid #ff5e1f';
        banner.style.borderRadius = '8px';
        banner.style.textAlign = 'center';
        banner.style.maxWidth = '800px';
        banner.style.color = 'var(--text-primary)';
        banner.style.boxShadow = '0 4px 15px rgba(255, 94, 31, 0.1)';
        banner.style.fontFamily = 'sans-serif';

        const authUrl = 'https://giscus.app/api/oauth/authorize?redirect_uri=' + encodeURIComponent(window.location.href) + '#comments';

        banner.innerHTML = `
            <p style="margin: 0 0 8px 0; font-size: 1.1em; line-height: 1.5; font-weight: bold; color: #ff5e1f;">
                💬 Comments having trouble loading?
            </p>
            <p style="margin: 0 0 16px 0; font-size: 0.9em; opacity: 0.9; line-height: 1.5; text-align: left;">
                This happens because the comments section is temporarily rate-limited. 
                To view or write comments, please log in, or open the discussion page directly.
            </p>
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                <a href="${authUrl}" style="display: inline-block; padding: 10px 20px; background-color: #ff5e1f; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s; cursor: pointer;">
                    Log In to view comments
                </a>
                <a href="${githubDiscussionUrl}" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 10px 20px; background-color: #333; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s; cursor: pointer; border: 1px solid #555;">
                    Open Discussion Page
                </a>
            </div>
        `;

        commentsDiv.parentNode.insertBefore(banner, commentsDiv);
    }

    // 1. Listen for Giscus postMessages
    window.addEventListener('message', (event) => {
        if (event.origin !== 'https://giscus.app') return;

        const { data } = event;
        if (!(typeof data === 'object' && data.giscus)) return;

        const giscusData = data.giscus;

        // Detect rate limiting or other Giscus errors
        if (giscusData.error) {
            console.warn('Giscus error detected:', giscusData.error);
            
            // Hide the Giscus iframe so the reader doesn't see the raw Giscus rate limit message
            const commentsDiv = document.getElementById('comments');
            if (commentsDiv) {
                const iframe = commentsDiv.querySelector('iframe.giscus-frame') || commentsDiv.querySelector('iframe');
                if (iframe) iframe.style.display = 'none';
            }
            
            showGiscusAuthBanner();
        } else if (giscusData.discussion || giscusData.resizeHeight) {
            giscusLoaded = true;
        }

        // Log viewer status
        if (giscusData.viewer) {
            if (!giscusData.viewer.login) {
                console.log('Giscus status: Reader is not logged in to GitHub.');
            } else {
                console.log('Giscus status: Reader is logged in to GitHub as ' + giscusData.viewer.login);
            }
        }
    });

    // 2. Fallback timeout: if Giscus doesn't load within 4 seconds, show authorization tip
    window.addEventListener('load', () => {
        setTimeout(() => {
            const commentsDiv = document.getElementById('comments');
            if (commentsDiv && !giscusLoaded) {
                console.log('Giscus loading timed out (4s), showing authorization banner.');
                
                // Hide the Giscus iframe if it exists so it doesn't show raw errors or loading spin
                const iframe = commentsDiv.querySelector('iframe.giscus-frame') || commentsDiv.querySelector('iframe');
                if (iframe) iframe.style.display = 'none';
                
                showGiscusAuthBanner();
            }
        }, 4000);
    });
})();


// Dynamic Banner Injection
(function() {
    const bannerContainer = document.getElementById('chapter-banner');
    if (!bannerContainer) return;

    const current = parseInt(bannerContainer.dataset.current);
    const first = parseInt(bannerContainer.dataset.first) || 1;
    const last = parseInt(bannerContainer.dataset.last) || 490;

    const DONATION_BANNER = `
    <div class="donation-banner" style="margin: 20px auto; padding: 15px 20px; background-color: var(--primary); border: 1px solid #ffb74d; border-radius: 8px; text-align: center; max-width: 800px; color: var(--text-primary); box-shadow: 0 4px 15px rgba(255, 183, 77, 0.08); font-family: sans-serif;">
        <p style="margin: 0 0 6px 0; font-size: 1em; line-height: 1.5;">💖 <strong>This site is maintained by Readers like you!</strong></p>
        <p style="margin: 0 0 12px 0; font-size: 0.85em; opacity: 0.8;">Hosting and domain costs are funded entirely through community donations.</p>
        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
            <a href="https://www.patreon.com/cw/LazyBittu" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #ffb74d; color: #1a1a2e; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Patreon</a>
            <a href="/donate" style="display: inline-block; padding: 8px 20px; background-color: #ff5e1f; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Donate</a>
            <a href="https://discord.gg/CZdNvKaNNr" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #5865F2; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Discord</a>
        </div>
    </div>`;

    const DISCORD_BANNER = `
    <div class="discord-banner" style="margin: 20px auto; padding: 15px 20px; background-color: var(--primary); border: 1px solid #5865F2; border-radius: 8px; text-align: center; max-width: 800px; color: var(--text-primary); box-shadow: 0 4px 15px rgba(88, 101, 242, 0.08); font-family: sans-serif;">
        <p style="margin: 0 0 6px 0; font-size: 1em; line-height: 1.5;">💬 <strong>Report issues on our Discord Server!</strong></p>
        <p style="margin: 0 0 12px 0; font-size: 0.85em; opacity: 0.8;">Connect with the community, share theories, and get notified about new chapters.</p>
        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
            <a href="https://discord.gg/CZdNvKaNNr" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #5865F2; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Join Discord</a>
            <a href="/donate" style="display: inline-block; padding: 8px 20px; background-color: #ff5e1f; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Donate</a>
        </div>
    </div>`;

    const LOTM_BANNER = `
    <div class="lotm-banner" style="margin: 20px auto; padding: 15px 20px; background-color: var(--primary); border: 1px solid #38bdf8; border-radius: 8px; text-align: center; max-width: 800px; color: var(--text-primary); box-shadow: 0 4px 15px rgba(56, 189, 248, 0.08); font-family: sans-serif;">
        <p style="margin: 0 0 6px 0; font-size: 1em; line-height: 1.5;">🧐 <strong>Looking for a change of pace? Read Lord of the Mysteries!</strong></p>
        <p style="margin: 0 0 12px 0; font-size: 0.85em; opacity: 0.8;">Experience the journey of Klein Moretti on our beautifully formatted sister site.</p>
        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
            <a href="https://beyonder.pages.dev" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 20px; background-color: #0284c7; color: #fff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: opacity 0.3s;">Read LOTM</a>
        </div>
    </div>`;

    let selectedBanner = '';

    if (!isNaN(current)) {
        if (current <= first + 4) {
            selectedBanner = DISCORD_BANNER;
        } else if (current >= last - 4) {
            selectedBanner = DONATION_BANNER;
        } else {
            const rand = Math.random();
            if (rand < 0.4) {
                selectedBanner = DONATION_BANNER;
            } else if (rand < 0.8) {
                selectedBanner = DISCORD_BANNER;
            } else {
                selectedBanner = LOTM_BANNER;
            }
        }
    }

    bannerContainer.innerHTML = selectedBanner;
})();
