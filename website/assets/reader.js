function getReaderState() {
    try {
        const raw = localStorage.getItem('orv_reader_state');
        const state = raw ? JSON.parse(raw) : {};
        if (state.login === undefined || state.login === null) {
            state.login = false;
        }
        return state;
    } catch (e) {
        console.error('Error reading local storage state:', e);
        return { login: false };
    }
}

function saveReaderState(state) {
    try {
        localStorage.setItem('orv_reader_state', JSON.stringify(state));
    } catch (e) {
        console.error('Error saving local storage state:', e);
    }
}

function migrateLocalStorage() {
    try {
        const state = {};
        let migrated = false;

        const lastRead = localStorage.getItem('lastread');
        if (lastRead !== null) {
            state.lastread = lastRead;
            localStorage.removeItem('lastread');
            migrated = true;
        }

        const lastType = localStorage.getItem('lasttype');
        if (lastType !== null) {
            state.lasttype = lastType;
            localStorage.removeItem('lasttype');
            migrated = true;
        }

        const settings = localStorage.getItem('settings1');
        if (settings !== null) {
            try {
                state.settings = JSON.parse(settings);
            } catch (e) {}
            localStorage.removeItem('settings1');
            migrated = true;
        }

        const types = ['orv', 'side', 'cont'];
        state.scroll_positions = {};
        state.scroll_history = {};

        types.forEach(type => {
            const historyKey = `scroll_history_${type}`;
            const historyRaw = localStorage.getItem(historyKey);
            if (historyRaw !== null) {
                try {
                    const historyList = JSON.parse(historyRaw) || [];
                    state.scroll_history[type] = historyList;
                    
                    historyList.forEach(scrollKey => {
                        const val = localStorage.getItem(scrollKey);
                        if (val !== null) {
                            state.scroll_positions[scrollKey] = parseInt(val, 10);
                            localStorage.removeItem(scrollKey);
                        }
                    });
                } catch (e) {}
                localStorage.removeItem(historyKey);
                migrated = true;
            }
        });

        if (migrated) {
            const existing = JSON.parse(localStorage.getItem('orv_reader_state')) || {};
            const merged = {
                ...state,
                ...existing,
                settings: { ...state.settings, ...existing.settings },
                scroll_positions: { ...state.scroll_positions, ...existing.scroll_positions },
                scroll_history: { ...state.scroll_history, ...existing.scroll_history }
            };
            localStorage.setItem('orv_reader_state', JSON.stringify(merged));
        }
    } catch (e) {
        console.error('Error during local storage migration:', e);
    }
}

// Run migration immediately
migrateLocalStorage();

function changeGiscusTheme(theme) {
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

    console.log('Giscus theme updated.');
}

setInterval(() => {
    changeGiscusTheme(window.theme);
}, 2000);

function updateLastReadState() {
    const scriptElement = document.getElementById('main-script');
    if (!scriptElement) return;
    let index = scriptElement.dataset.index;
    let type = scriptElement.dataset.type;
    let state = getReaderState();
    state.lastread = String(index);
    state.lasttype = String(type);
    saveReaderState(state);
}

setTimeout(updateLastReadState, 10000);

function classChangeTheme(elementClass, elemetTheme) {
    let element = document.getElementsByClassName(elementClass);

    Array.from(element).forEach(item => {
        item.classList.remove("theme1", "theme2", "theme3", "theme4", "theme5", "theme6");
        item.classList.add(elemetTheme);
    });
}

function loadSettingsFromLocalStorage() {
    try {
        let state = getReaderState();
        let settings = state.settings;

        if (!settings) return null;

        if (settings.theme) {
            const el = document.getElementById('set-theme');
            if (el) el.value = settings.theme;
        }
        if (settings.font) {
            const el = document.getElementById('set-font');
            if (el) el.value = settings.font;
        }
        if (settings.fontSize) {
            if (settings.fontSize == 52) { settings.fontSize = 51; }
            const el = document.getElementById('set-font-size');
            if (el) el.value = settings.fontSize;
        }
        if (settings.fontWeight) {
            const el = document.getElementById('set-font-weight');
            if (el) el.value = settings.fontWeight;
        }
        if (settings.lineHeight) {
            if (settings.lineHeight == 32) { settings.lineHeight = 49; }
            const el = document.getElementById('set-line-height');
            if (el) el.value = settings.lineHeight;
        }
        if (settings.richTextToggle !== undefined) {
            const el = document.getElementById('set-rich-text-toggle');
            if (el) el.checked = settings.richTextToggle;
        }
        if (settings.systemMsgStyle) {
            const el = document.getElementById('set-rich-system-msg');
            if (el) el.value = settings.systemMsgStyle;
        }
        if (settings.systemWindowStyle) {
            const el = document.getElementById('set-rich-system-window');
            if (el) el.value = settings.systemWindowStyle;
        }
        if (settings.constSpeechStyle) {
            const el = document.getElementById('set-rich-const');
            if (el) el.value = settings.constSpeechStyle;
        }
        if (settings.outerSpeechStyle) {
            const el = document.getElementById('set-rich-outer');
            if (el) el.value = settings.outerSpeechStyle;
        }
        if (settings.quoteStyle) {
            const el = document.getElementById('set-rich-quote');
            if (el) el.value = settings.quoteStyle;
        }
        if (settings.noticeStyle) {
            const el = document.getElementById('set-rich-notice');
            if (el) el.value = settings.noticeStyle;
        }
        if (settings.genericBoxStyle) {
            const el = document.getElementById('set-rich-box');
            if (el) el.value = settings.genericBoxStyle;
        }

        return settings;
    } catch (error) {
        console.error('Error loading settings from local storage:', error);
        return {};
    }
}

loadSettingsFromLocalStorage();

window.theme = "dark";

document.addEventListener('DOMContentLoaded', function () {
    const settingsForm = document.getElementById('settings-form');

    function applySettings() {
        let root = document.documentElement;
        let themeEl = document.getElementById('set-theme');
        let theme = themeEl ? themeEl.value : "dark";
        let font = document.getElementById('set-font')?.value || "sans-serif";
        let fontSize = document.getElementById('set-font-size')?.value || 50;
        let fontWeight = document.getElementById('set-font-weight')?.value || 400;
        let lineHeight = document.getElementById('set-line-height')?.value || 50;
        let richTextToggle = document.getElementById('set-rich-text-toggle')?.checked ?? true;
        
        let systemMsgStyle = document.getElementById('set-rich-system-msg')?.value || "theme1";
        let systemWindowStyle = document.getElementById('set-rich-system-window')?.value || "theme1";
        let constSpeechStyle = document.getElementById('set-rich-const')?.value || "theme1";
        let outerSpeechStyle = document.getElementById('set-rich-outer')?.value || "theme1";
        let quoteStyle = document.getElementById('set-rich-quote')?.value || "theme1";
        let noticeStyle = document.getElementById('set-rich-notice')?.value || "theme1";
        let genericBoxStyle = document.getElementById('set-rich-box')?.value || "theme1";

        if (fontSize < 30) { fontSize = 30; }
        if (fontSize > 100) { fontSize = 100; }
        fontSize = (fontSize / 3) + "px";

        if (lineHeight > 100) { lineHeight = 100; }
        if (lineHeight < 1) { lineHeight = 1; }
        lineHeight = lineHeight / 30.625;
        root.style.setProperty('--line-space', lineHeight + "rem");

        window.theme = theme;
        changeGiscusTheme(theme);

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
        document.body.style.fontWeight = fontWeight;

        const settings = {
            theme,
            font,
            fontSize: document.getElementById('set-font-size')?.value,
            fontWeight,
            lineHeight: document.getElementById('set-line-height')?.value,
            richTextToggle,
            systemMsgStyle,
            systemWindowStyle,
            constSpeechStyle,
            outerSpeechStyle,
            quoteStyle,
            noticeStyle,
            genericBoxStyle,
        };

        try {
            let state = getReaderState();
            state.settings = settings;
            saveReaderState(state);
        } catch (error) {
            console.error('Error saving settings to local storage:', error);
        }

        const richMsg = document.getElementById('set-rich-system-msg');
        const richWin = document.getElementById('set-rich-system-window');
        const richConst = document.getElementById('set-rich-const');
        const richOuter = document.getElementById('set-rich-outer');
        const richQuote = document.getElementById('set-rich-quote');
        const richNotice = document.getElementById('set-rich-notice');
        const richBox = document.getElementById('set-rich-box');

        if (richTextToggle) {
            if (richMsg) richMsg.disabled = false;
            if (richWin) richWin.disabled = false;
            if (richConst) richConst.disabled = false;
            if (richOuter) richOuter.disabled = false;
            if (richQuote) richQuote.disabled = false;
            if (richNotice) richNotice.disabled = false;
            if (richBox) richBox.disabled = false;
        } else {
            if (richMsg) richMsg.disabled = true;
            if (richWin) richWin.disabled = true;
            if (richConst) richConst.disabled = true;
            if (richOuter) richOuter.disabled = true;
            if (richQuote) richQuote.disabled = true;
            if (richNotice) richNotice.disabled = true;
            if (richBox) richBox.disabled = true;

            systemMsgStyle = "theme1";
            systemWindowStyle = "theme1";
            constSpeechStyle = "theme1";
            outerSpeechStyle = "theme1";
            quoteStyle = "theme1";
            noticeStyle = "theme1";
            genericBoxStyle = "theme1";
        }

        classChangeTheme("orv_system", systemMsgStyle);
        classChangeTheme("orv_window", systemWindowStyle);
        classChangeTheme("orv_constellation", constSpeechStyle);
        classChangeTheme("orv_outergod", outerSpeechStyle);
        classChangeTheme("orv_quote", quoteStyle);
        classChangeTheme("orv_notice", noticeStyle);
        classChangeTheme("orv_box", genericBoxStyle);
    }

    applySettings();
    window.applySettings = applySettings;

    if (settingsForm) {
        settingsForm.addEventListener('change', applySettings);
        settingsForm.addEventListener('reset', () => setTimeout(applySettings, 0));
    }

    document.getElementById('set-font-size')?.addEventListener('input', applySettings);
    document.getElementById('set-font-weight')?.addEventListener('input', applySettings);
    document.getElementById('set-line-height')?.addEventListener('input', applySettings);

    function restoreScroll() {
        const scriptElement = document.getElementById('main-script');
        if (!scriptElement) return;
        const index = scriptElement.dataset.index;
        const type = scriptElement.dataset.type;
        const scrollKey = `scrollY_${type}_${index}`;

        try {
            let state = getReaderState();
            const savedScroll = state.scroll_positions ? state.scroll_positions[scrollKey] : undefined;
            if (savedScroll !== undefined && savedScroll !== null) {
                window.scrollTo(0, parseInt(savedScroll, 10));
            } else {
                window.scrollTo(0, 0);
            }
        } catch (e) {
            console.error('Error restoring scroll:', e);
        }
    }

    restoreScroll();

    function saveScrollPosition() {
        const scriptElement = document.getElementById('main-script');
        if (!scriptElement) return;
        const index = scriptElement.dataset.index;
        const type = scriptElement.dataset.type;
        const scrollKey = `scrollY_${type}_${index}`;

        try {
            let state = getReaderState();
            if (!state.scroll_positions) state.scroll_positions = {};
            if (!state.scroll_history) state.scroll_history = {};

            state.scroll_positions[scrollKey] = window.scrollY;

            let history = state.scroll_history[type] || [];
            history = history.filter(key => key !== scrollKey);
            history.unshift(scrollKey);

            const MAX_HISTORY_SIZE = 5;
            while (history.length > MAX_HISTORY_SIZE) {
                const oldestKey = history.pop();
                delete state.scroll_positions[oldestKey];
            }

            state.scroll_history[type] = history;
            saveReaderState(state);
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

    // ==========================================
    // DYNAMIC CHAPTER NAVIGATION (SPA ROUTER)
    // ==========================================
    async function loadChapter(url) {
        try {
            saveScrollPosition(); // Save position for current chapter before navigating

            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to fetch chapter');
            const html = await response.text();

            const parser = new DOMParser();
            const newDoc = parser.parseFromString(html, 'text/html');

            // 1. Swap main content
            const oldMain = document.querySelector('.orv_main');
            const newMain = newDoc.querySelector('.orv_main');
            if (oldMain && newMain) oldMain.innerHTML = newMain.innerHTML;

            // 2. Swap chapter change navigation links
            const oldChangeCh = document.querySelector('.change-ch');
            const newChangeCh = newDoc.querySelector('.change-ch');
            if (oldChangeCh && newChangeCh) oldChangeCh.innerHTML = newChangeCh.innerHTML;

            // 3. Update dataset on script tag
            const oldScript = document.getElementById('main-script');
            const newScript = newDoc.getElementById('main-script');
            if (oldScript && newScript) {
                oldScript.dataset.index = newScript.dataset.index;
                oldScript.dataset.type = newScript.dataset.type;
                oldScript.dataset.titles = newScript.dataset.titles;
            }

            // 4. Update Document Metadata & URL History
            document.title = newDoc.title;
            history.pushState(null, '', url);

            // 5. Re-apply Settings & Restore Scroll / State
            applySettings();
            restoreScroll();
            updateLastReadState();

            // 6. Close Modal Menu if Open
            const modal = document.getElementById('chapters');
            if (modal) modal.style.display = 'none';

        } catch (err) {
            console.error('Error swapping chapter dynamically:', err);
            window.location.href = url; // Fallback to traditional reload on failure
        }
    }

    // Intercept clicks on links matching chapter transitions
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (!link) return;

        const href = link.getAttribute('href');
        if (href && (href.includes('./ch_') || href.includes('/ch_') || link.closest('.change-ch'))) {
            e.preventDefault();
            loadChapter(link.href);
        }
    });

    // Handle Browser Back / Forward buttons
    window.addEventListener('popstate', () => {
        loadChapter(window.location.href);
    });
});

let chFetchStatus = false;
const ChapterList = [];

function addAllChapters() {
    const scriptElement = document.getElementById('main-script');
    if (!scriptElement) return;
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
                let titleEl = document.getElementsByClassName("orv_title")[0];
                if (!chapterSearch || !titleEl) return;

                let chapterTitle = titleEl.textContent.trim();
                let chapterID = "";
                let chSearchresult = [];

                ChapterList.forEach(chapter => {
                    if (chapterTitle === chapter.title) {
                        chapterID = "current-chapter";
                        chapter.index = "";
                    }
                    chSearchresult.push(`<div class="chapter_item" id="${chapterID}"><a href="./ch_${chapter.index + 1}"><p>${chapter.title}</p></a></div>`);
                    chapterID = "";
                });

                chapterSearch.innerHTML = chSearchresult.join("");
                const currentCh = document.getElementById("current-chapter");
                if (currentCh) currentCh.scrollIntoView({ behavior: "smooth", block: "center" });
            });
    }
}

function openChapters() {
    addAllChapters();
    const chaptersModal = document.getElementById('chapters');
    if (chaptersModal) chaptersModal.style.display = 'block';
}

function findChapter() {
    let chapter = document.getElementById("find-chapter").value.trim();
    let chapterSearch = document.getElementById("chapter-search-reasult");
    if (!chapterSearch) return;

    chapterSearch.innerHTML = "";
    let chSearchresult = [];

    for (let i = 0; i < ChapterList.length; i++) {
        let displayTitle = String(ChapterList[i].title);
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

window.addEventListener('load', requestWakeLock);

document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        requestWakeLock();
    }
});

window.addEventListener('beforeunload', releaseWakeLock);
window.addEventListener('popstate', releaseWakeLock);
