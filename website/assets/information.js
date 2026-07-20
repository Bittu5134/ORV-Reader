let ChapterList = [];
let ongoing = false;
const script = document.getElementById('main-script');

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

document.addEventListener('DOMContentLoaded', function () {
    migrateLocalStorage();
    const state = getReaderState();
    const LastRead = parseInt(state.lastread)
    const lastType = state.lasttype

    console.log(LastRead, lastType)

    if (LastRead !== undefined && !isNaN(LastRead) && lastType === script.dataset.type) {
        const readbtn = document.getElementById("read");
        const reada = document.getElementById("read-a");

        reada.href = `./read/ch_${LastRead + 1}`;
        readbtn.textContent = "Continue";
    }
});

function addAllChapters() {
    fetch(script.dataset.title)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            ChapterList.push(...data);
            ChapterList = ChapterList.slice().sort((a, b) => b.index - a.index)
            console.log("Chapters loaded:", ChapterList);
            if (ongoing){
                // ChapterList.reverse();
                displayChapters();}else{filter()}
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function addMeta() {
    fetch(script.dataset.meta)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const info = document.getElementsByClassName("status")[0];
            console.log(data);
            if (data.status === "Ongoing"){ongoing=true}
            info.innerHTML = `
            <p>${data.title}</p>
            <p>Author: ${data.author}<br>
                Chapters: ${data.chapters}<br>
                Status: ${data.status}</p>`
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function displayChapters() {
    let chapterSearch = document.getElementById("chapter-result");
    chapterSearch.innerHTML = "";
    let chSearchresult = [];

    ChapterList.forEach(chapter => {
        chSearchresult.push(`<div class="chapter_item"><a href="./read/ch_${chapter.index + 1}"><p>${chapter.title}</p></a></div>`);
    });

    chapterSearch.innerHTML = chSearchresult.join("");
}

function filter() {
    ChapterList = ChapterList.slice().reverse();
    document.getElementById("search").value = ""
    console.log(document.getElementById("filter").style.transform)
    const FilterSVG = document.getElementById("filter");
    if (FilterSVG.style.transform === "rotateX(180deg)") {
        FilterSVG.style.transform = "rotateX(0deg)"
    } else {
        FilterSVG.style.transform = "rotateX(180deg)"
    }
    displayChapters()

}


function findChapter(value) {
    let chapterSearch = document.getElementById("chapter-result");
    chapterSearch.innerHTML = "";
    let chSearchresult = [];

    for (let i = 0; i < ChapterList.length; i++) {

        const displayTitle = String(ChapterList[i].title);
        let title = displayTitle.toLowerCase();
        let chSearchindex = title.indexOf(value.toLowerCase());
        let index = ChapterList[i].index;
        if (chSearchindex !== -1) {
            chSearchresult.push(`<div class="chapter_item"><a href="./read/ch_${index + 1}"><p>${displayTitle}</p></a></div>`);
        }
    }
    chapterSearch.innerHTML = chSearchresult.join("");

    if (chSearchresult.length === 0) {
        chapterSearch.innerHTML = `<div class="chapter_item"><p>Chapter not found</p></div>`;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    addMeta();
    addAllChapters();
});
