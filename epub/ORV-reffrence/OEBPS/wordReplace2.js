String.prototype.remove = function (index, count) {
  return this.substring(0, index) + this.substring(index + count);
};

String.prototype.insert = function (index, string) {
  if (index > 0)
    return this.substring(0, index) + string + this.substring(index, this.length);
  else
    return string + this;
};

String.prototype.regexIndexOf = function (regex, startpos) {
  const indexOf = this.substring(startpos || 0).search(regex);
  return (indexOf >= 0) ? (indexOf + (startpos || 0)) : indexOf;
}

Array.prototype.extend = function (other_array) {
  /* you should include a test to check whether other_array really is an array */
  other_array.forEach(function (v) { this.push(v) }, this);
}

function escapeRegExp(string) {
  return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

function regexFromString(str) {
  const match = str.match(new RegExp('^/(.*?)/([gimy]*)$'));
  if (match === null) return /a^/;
  // Add /g and /m if they weren't specified
  if (match[2].indexOf('g') === -1) match[2] += 'g';
  if (match[2].indexOf('m') === -1) match[2] += 'm';

  try {
    return new RegExp(match[1], match[2]);
  }
  catch (err) {
    // Just drop it and return an empty replacement.
    if (err.name == 'SyntaxError') return /b^/;
    else throw err;
  }
}

function mimicLetterCase(originalWord, replacement) {
  if (!originalWord.length) return originalWord;
  let allCaps = true, titleCase = true;

  // Isolated words that begin with a capital letter shall be titlecase by default and lowercase otherwise
  let _tcmatch = originalWord.search('/\s/') === -1;
  if (_tcmatch) {
    titleCase = allCaps = originalWord[0].toUpperCase() == originalWord[0];
  }
  for (let i = 0; i < originalWord.length; ++i) {
    // If this letter is lowercase
    if (allCaps && originalWord[i].toUpperCase() != originalWord[i]) {
      // Then the word can't be AllCaps
      allCaps = false;
      if (!titleCase) break;
    }
    // If what comes after a space is a lowercase letter, this isn't TitleCase
    else if (originalWord[i].search(/\s/) === 0) {
      // Skip any extra space up to the second to last character
      while (++i < originalWord.length - 2 && originalWord[i].search(/\s/) === 0);
      // If the next letter isn't an uppercase letter, this ain't no titlecase
      if (i >= originalWord.length || originalWord[i].search(/[A-Z]/) === -1) titleCase = false;
      if (!allCaps) break;
    }
  }

  let result = replacement;
  if (result.length == 0) return result;
  // All-Caps
  if (allCaps) {
    result = result.toUpperCase();
  }
  // TitleCase
  else if (titleCase) {
    result = result.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
  }
  // First Uppercase
  else if (originalWord[0].toUpperCase() == originalWord[0]) {
    result = result[0].toUpperCase() + result.substring(1).toLowerCase();
  }
  // Lowercase
  else {
    result = result.toLowerCase();
  }
  return result;
}

function replaceBackreferences(word, replacement) {
  let regexp = regexFromString(replacement.repA);

  let match = regexp.exec(word);
  // Get the content of each capturing group and replace any backreference in the replacement with it
  let _rep = replacement.repB;
  for (let j = 1; j < match.length; ++j) {
    if (!match[j]) continue;
    let br_i;
    while ((br_i = _rep.indexOf("\\" + j)) !== -1) {
      if (br_i > 0 && _rep[br_i - 1] == '\\') continue;

      _rep = _rep.remove(br_i, 2).insert(br_i, match[j]);
    }

  }
  return _rep;
}

function parseTokens(word, repB, replacement) {
  let original = replacement.repB; // The un-modified repB.
  // The empty space is because [^\\] matches anything BUT a \, but it doesn't work if there isn't a character to begin with.
  // A ? would make the match's length inconsistent, so fuck it.
  let tokens = (' ' + original).match(/[^\\]\\(C|L|I|E)/gi);
  if (!tokens) return repB;

  let index, oIndex;
  let _lastTest, _lastIndex, _xpBackref;
  tokens.forEach(function (v) {
    v = v.substring(1).toLowerCase();

    index = repB.toLowerCase().indexOf(v); // No starting position because the processed flags are already removed
    oIndex = original.toLowerCase().indexOf(v, oIndex + 1); // Starting position because original should stay intact

    if (index === -1) return; // Ex. when a successful if removes its else.

    repB = repB.remove(index, 2); // Remove the matched token.
    switch (v[1]) {
      case 'c': // Maintain (c)ase of the next word
        let endOfWord = repB.regexIndexOf(/(\W|$)/, index);
        let oEndOfWord = original.regexIndexOf(/(\W|$)/, oIndex + 2);

        repB = repB.remove(index, endOfWord - index).insert(index, original.substring(oIndex + 2, oEndOfWord));
        break;
      case 'l': // Maintain case of the next letter
        repB = repB.remove(index, 1).insert(index, original.substring(oIndex + 2, oIndex + 3));
        break;
      case 'i': // If the following capturing group was NOT matched, then insert... [Syntax: \I\1:whatever;\E:Also whatever;]
        _lastIndex = index;
        _lastTest = !/\\[1-9][0-9]?/.test(repB.substring(index, index + 2));

        // Expand the backreference from the original replacement
        _xpBackref = replaceBackreferences(word, { repA: replacement.repA, repB: original.substring(oIndex + 2, oIndex + 4) });
        // Apply the correct letter casing by giving it some context and then slicing it off
        let _contextualized = (repB[index - 1] || ' ') + _xpBackref;
        _xpBackref = mimicLetterCase(word, _contextualized).substring(1);
      case 'e': // Else, insert...

        if (v[1] == 'i') {
          // Remove the 'if' block but not its contents unless the test failed.
          // At this point we removed everything up to the colon, the easy part
          repB = repB.substring(0, index) + repB.substring(index + _xpBackref.length + 1);

          let _nesIndex = repB.regexIndexOf(/[^\\];/, index) + 1;
          // If the test failed, remove everything up to the semicolon
          if (!_lastTest) {
            repB = repB.remove(index, _nesIndex - index + 1);
          }
          // Otherwise just remove the semicolon
          else {
            repB = repB.remove(_nesIndex, 1);
            // And apply proper capitalization to the contents of this if
            if (replacement.case == 'Maintain') {
              let wordToCapitalize = index > 0 ? repB.substring(index - 1, _nesIndex) : ' ' + repB.substring(index, _nesIndex);
              wordToCapitalize = mimicLetterCase(word, wordToCapitalize).substring(1);
              repB = repB.remove(index, wordToCapitalize.length).insert(index, wordToCapitalize);
            }
          }
        }
        else if (v[1] == 'e') {
          // Remove the 'else' block but not its contents.
          // Again, remove up to the colon, which is easy (the colon IS expected to be exactly adjacent to the \E)
          repB = repB.substring(0, index) + repB.substring(index + 1);

          let _nesIndex = repB.regexIndexOf(/[^\\];/, index) + 1;
          // If the earlier test succeeded, remove everything up to the semicolon
          if (_lastTest) {
            repB = repB.remove(index, _nesIndex - index + 1);
          }
          // Otherwise only remove the semicolon
          else {
            repB = repB.remove(_nesIndex, 1);
            // And apply proper capitalization to the contents of this else
            if (replacement.case == 'Maintain') {
              let wordToCapitalize = index > 0 ? repB.substring(index - 1, _nesIndex) : ' ' + repB.substring(index, _nesIndex);
              wordToCapitalize = mimicLetterCase(word, wordToCapitalize).substring(1);
              repB = repB.remove(index, wordToCapitalize.length).insert(index, wordToCapitalize);
            }
          }
        }
        break;
    }

  });

  return repB;
}
function _replace(str, word, replacement, _repB) {
  let repB = _repB || replacement.repB;
  if (replacement.case == 'Maintain') repB = mimicLetterCase(word, repB);
  // This function parses specials tokens such as \C for maintaining case on a specific word.
  repB = parseTokens(word, repB, replacement);

  try {
    str = str.replace(new RegExp(escapeRegExp(word), 'g'), repB);
  }
  catch (err) {
    if (err.name == 'RangeError');
    else throw err;
  }
  return str;
}

function tryReplacement(source, replacement) {
  let replacedsource = source;
  let repB = replacement.repB;

  switch (replacement.type) {
    case 'Simple':
      const expS = new RegExp(escapeRegExp(replacement.repA), 'gim');
      let matchS = expS.exec(replacedsource);

      while (matchS != null) {
        let replacedPart = _replace(replacedsource.substring(matchS.index, matchS.index + matchS[0].length), matchS[0], replacement);
        replacedsource = replacedsource.substring(0, matchS.index) + replacedPart + replacedsource.substring(matchS.index + matchS[0].length);

        expS.lastIndex -= (matchS[0].length - replacedPart.length);
        matchS = expS.exec(replacedsource);
      }

      return replacedsource;
    case 'RegEx':
      const expR = regexFromString(replacement.repA);
      let matchR = expR.exec(replacedsource);

      while (matchR != null) {
        repB = replaceBackreferences(matchR[0], replacement);

        let replacedPart = _replace(replacedsource.substring(matchR.index, matchR.index + matchR[0].length), matchR[0], replacement, repB);
        replacedsource = replacedsource.substring(0, matchR.index) + replacedPart + replacedsource.substring(matchR.index + matchR[0].length);

        expR.lastIndex -= (matchR[0].length - replacedPart.length);
        matchR = expR.exec(replacedsource);
      }

      return replacedsource;
    case 'Swap':
      // For swaps we'll do something less obvious but actually simpler: exactly what you had to do in WR1, but programmatically.
      // No extra code, no extra tears.

      let _swapReplacementA = { repA: replacement.repA, repB: mimicLetterCase(replacement.repA, 'WR SWAP TEMP__'), type: 'Simple', case: replacement.case };
      let _swapReplacementB = { repA: replacement.repB, repB: replacement.repA, type: 'Simple', case: replacement.case };
      let _swapReplacementC = { repA: mimicLetterCase(replacement.repB, 'WR SWAP TEMP__'), repB: replacement.repB, type: 'Simple', case: replacement.case };

      replacedsource = tryReplacement(source, _swapReplacementA);
      replacedsource = tryReplacement(replacedsource, _swapReplacementB);
      replacedsource = tryReplacement(replacedsource, _swapReplacementC);

      return replacedsource;
  }
}

let g_replacements;

function applyReplacements(node) {
  // Apply each replacement in order
  g_replacements.forEach(function (replacement) {
    if (!replacement.active) return;
    node = tryReplacement(node, replacement);
  });
  return node;
}

function processMutations(mutations) {
  mutations.forEach(function (mut) {
    switch (mut.type) {
      case 'characterData':
        applyReplacements(mut.target);
        break;
      case 'childList':
        $(mut.addedNodes).each(function (i, node) { applyReplacements($(node).find('*')); });
        break;
    }
  });
}

function importReplecemets(jsonFilename) {
  let jsnSettings = {};
  let newSettings = [];

  try {
    jsnSettings = require(jsonFilename);
  } catch (err) {
    console.log(err);
    return;
  }

  // WR 2-style syntax
  if (jsnSettings.version && jsnSettings.version.indexOf('2.') !== -1) {
    let values = jsnSettings.replacements;

    for (let i = 0; i < values.length; ++i) {
      newSettings.push({
        repA: values[i].repA,
        repB: values[i].repB,
        type: values[i].type,
        case: values[i].case,
        active: values[i].active
      });
    }
  }
  else {
    console.log('Unrecognized format!');
    return;
  }

  return newSettings;
}

function importFootnotes(jsonFilename) {
  let jsnFootnotes = {};

  try {
    jsnFootnotes = require(jsonFilename);
  } catch (err) {
    console.log(err);
    return;
  }

  return jsnFootnotes.endnotes;
}

function replaceWithJson(fileName, settings) {
  g_replacements = settings;
  // Return if there are no replacements
  if (!g_replacements || !g_replacements.length) {
    console.log('No replacements loaded!');
    return;
  }

  const data = readFile(fileName);
  if (!data) {
    return;
  }

  // Apply the replacements once upon injection to each descendant of body
  result = applyReplacements(data);
  // console.log(result);

  const fs = require('fs');
  fs.writeFileSync(fileName, result);
}

function readFile(fileName) {
  const fs = require('fs');

  try {
    const data = fs.readFileSync(fileName, 'utf8');
    // console.log(data);
    console.log('File loaded: ', fileName);
    return data
  } catch (e) {
    console.log('Error:', e.stack);
    return;
  }
}

function padString(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function injectFootnotes(fileName, chapNum, footnotesArr) {
  let data = readFile(fileName);
  if (!data) {
    return;
  }

  let endnoteSecStart = "<br />\n<hr />\n<section epub:type='endnotes' role='doc-endnotes'>\n";
  let endnotesStr = "";
  footnotesArr.forEach(function (value, i) {
    const iN = i + 1
    endnotesStr += "<aside id='note" + iN + "' epub:type='footnote'>\n";
    endnotesStr += "<a href='chap_00" + padString(chapNum, 3) + ".xhtml#ref" + iN + "'>[" + iN + "]</a> ";
    endnotesStr += value + "\n"
    endnotesStr += "</aside>\n";
  });
  let endnoteSecEnd = "</section>\n";

  const repB = endnoteSecStart + endnotesStr + endnoteSecEnd + "</body>";
  const replacedSource = data.replace("</body>", repB);

  const fs = require('fs');
  fs.writeFileSync(fileName, replacedSource);
}

function runReplacersForFile(
  fileName,
  repList,
  illustrationsList = null,
  injectIllustrations = false,
  footnotes = null,
  chapI = null) {
    replaceWithJson(fileName, repList);

    if (injectIllustrations) {
        replaceWithJson(fileName, illustrationsList);
    }

    if (chapI != null && footnotes != null && !!footnotes[chapI]) {
        let notes = footnotes[chapI]
        injectFootnotes(fileName, chapI, notes);
    }
}

function main() {
  console.time("Replacements took");

  let filenameBase = (process.argv[2] != null && process.argv[2] != "default") ? process.argv[2] : 'FIN-Kieran/OEBPS';
  let repList = importReplecemets('../replacements/word-replace.json');
  let illustrationsList = importReplecemets('../replacements/image-injection.json');
  let footnotes = importFootnotes('../replacements/footn-injection.json');

  let injectIllustrations = (process.argv[3] == "illustrated");

  for (let i = 1; i <= 551; ++i) {
    let fileName = filenameBase + '/chap_00' + padString(i, 3) + '.xhtml'
    runReplacersForFile(fileName, repList, illustrationsList, injectIllustrations, footnotes, i);
  }
  const navFile = filenameBase + '/nav.xhtml';
  runReplacersForFile(navFile, repList);
  const tocFile = filenameBase + '/toc.ncx';
  runReplacersForFile(tocFile, repList);

  console.timeEnd("Replacements took");
}

main();
