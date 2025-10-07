let ChapterList = [];
let ongoing = false;
const script = document.getElementById('main-script');

document.addEventListener('DOMContentLoaded', function () {
    const LastRead = parseInt(localStorage.getItem("lastread"))
    const lastType = localStorage.getItem("lasttype")

    console.log(LastRead, lastType)

    if (LastRead && lastType === script.dataset.type) {
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
