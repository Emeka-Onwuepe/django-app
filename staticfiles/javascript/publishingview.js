copyRightDate(2020)

function copyRightDate(x) {
    var d = new Date;
    var year = d.getFullYear();
    var footerDate = document.getElementById("footerdate");
    if (year == x) {
        footerDate.innerHTML = year;
    } else {
        footerDate.innerHTML = x + "-" +
            year;
    }
}

let title = document.querySelector('#id_title')
let titleSlug = document.querySelector('#id_title_slug')

function urlSlug() {
    let titlesmatch = title.value.match(/\w+/ig)
    if (titlesmatch != null) {
        let titleslugs = titlesmatch.filter(x => x.toLowerCase()).join("-");
        titleSlug.value = titleslugs
        if (titleslugs.length > 50) {
            let slugLimit = titleslugs.slice(0, 50);
            titleSlug.value = slugLimit
            if (/-$/.test(slugLimit)) {
                let slugLimitCorrection = slugLimit.slice(0, this.length - 1)
                titleSlug.value = slugLimitCorrection
            }
        }
    } else {
        titleSlug.value = ""
    }
}

title.addEventListener("keyup", function() {
    urlSlug();
})



let addSection = document.querySelector('#addSection')

function Addsection() {
    let sectionDiv = document.querySelector('#addsection')
    let subSection = document.querySelector('.subsection').innerHTML
    let totalForm = document.querySelector("#id_sections-TOTAL_FORMS").value
    let totalFormInt = parseInt(totalForm, 10)
    let number = totalFormInt
    let div = document.createElement('div');
    div.className = "subsection"
    let buttom = document.createElement('button')
    buttom.id = `section-${number}`
    buttom.innerHTML = "Delete"
    let literal = `sections-${number}`
    let subsectionRefined = subSection.replace(/-*sections-\d+/ig, literal)
        .replace(/(contenteditable.*?>)(.*)(<\/div>)/ig, "$1$3")
        .replace(/(<input.*value=")(.*?)(".*>)/ig, "$1$3")
        .replace(/(Currently.*)\s*(.*)\s*(<label.*)\s*change:/ig, "")
    div.innerHTML = subsectionRefined
    div.appendChild(buttom)
    sectionDiv.appendChild(div)
    document.querySelector("#id_sections-TOTAL_FORMS").value = totalFormInt + 1
    buttom.onclick = function(event) {
        event.preventDefault();
        div.style.display = "none"
        div.lastElementChild.previousElementSibling
            .lastElementChild.previousElementSibling
            .lastElementChild.checked = true
    }
    console.log(document.querySelector("#id_sections-TOTAL_FORMS").value)
}

addSection.addEventListener("click", function() {
    Addsection();

})

// let fileInputs = document.querySelectorAll("input[type='file']")
// let verify = true
// let allowedImageSize = 150
//     //console.log(fileInputs)
// for (const images of fileInputs) {
//     images.addEventListener("change", function() {
//         let image = this.files[0]
//         let int = parseInt(image.size / 1024)
//         if (int >= allowedImageSize) {
//             verify = false
//             alert(`You uploaded an image greater than ${allowedImageSize}KB. Please change the image or reduce the image size`)
//         } else {
//             verify = true
//         }

//     }, false)
// }

replaceTextArea()

function replaceTextArea() {
    let textarea = document.querySelectorAll("textarea")
    let divEditor = document.createElement("div")
    divEditor.contentEditable = true
    divEditor.className = "divEditor"
    divEditor.style.border = "3px solid green"
    for (const area of textarea) {
        area.style.display = "none"
        let parentNode = area.parentNode
        if (area.nextElementSibling != divEditor.cloneNode()) {
            parentNode.insertBefore(divEditor.cloneNode(), area.nextSibling.nextSibling)
        }
    }
}

copyToDiv()

function copyToDiv() {
    let textarea = document.querySelectorAll("textarea")
    for (const area of textarea) {
        if (area.innerHTML.length > 0) {
            let data = area.value.replace(/p>/ig, 'div>')
            let div = document.createElement("div")
            div.innerHTML = data
            area.nextElementSibling.appendChild(div)
        }
    }
}

function processData() {
    let divEditor = document.querySelectorAll(".divEditor")
    for (const editor of divEditor) {
        //change all Div tags to Paragraph tags
        let editorData = editor.innerHTML.replace(/div>/ig, 'p>')
            //tag an untaged data at the end with a paragrapy tag
            //especially when paste function is used
        let Data = editorData;
        if (!/p>$/.test(editorData)) {
            Data = editorData.replace(/(.+p>)(.+)$/, "$1<p>$2</p>")
        }
        //remove emty tags and collaspe white spaces
        let fData = Data.replace(/<p><br\/?p>|<br.*?>|&nbsp;;*?/ig, "").replace(/<p>\s*<\/p>*/ig, "")
            //remove the outer Div/P on article edit
        let finalData = fData
        if (/^<p><p>|<\/p><\/p>$/ig.test(fData)) {
            finalData = fData.replace(/^<p>|<\/p>$/ig, "")
        }
        //assign to data to textareas
        editor.previousElementSibling.innerHTML = finalData
            //empty every DivEditor
            //editor.innerHTML=""
        console.log(editor.previousElementSibling.innerHTML)
    }
    //send data to the database
    // if (!verify) {
    //     alert(`Unable to submit. There is an image(s) higher than ${allowedImageSize}KB in your article.`)
    // }
    // return verify
}
//assign execCommand to buttons onclick
let buttons = document.querySelectorAll(".tool-btn")
for (const button of buttons) {
    button.addEventListener("click", () => {
        let cmd = button.dataset["command"]
        if (cmd === "createLInk") {
            let url = prompt("Enter a URl:", "https://")
            document.execCommand(cmd, false, url)
        } else if (cmd === "raisenumber") {
            let selected = window.getSelection().toString()
            if (window.Selection && parseInt(selected)) {
                document.execCommand("superscript", false, null)
                document.execCommand("createLInk", false, "#end_notes")
            }
        } else if (cmd === "removenumber") {
            let selected = window.getSelection().toString()
            if (window.Selection && parseInt(selected)) {
                let intId = parseInt(selected)
                document.execCommand("unlink", false, null)
                document.execCommand("superscript", false, null)
                window.getSelection().deleteFromDocument()
                window.getSelection().removeAllRanges()
            }
        } else {
            document.execCommand(cmd, false, null)
        }
    })
}

let divEditors = document.querySelectorAll(".divEditor")
for (const divEditor of divEditors) {

    divEditor.addEventListener("paste", function(event) {
        let paste = (event.clipboardData || window.clipboardData).getData('text')
        console.log(paste)
        const selection = window.getSelection()
        if (!selection.rangeCount) return false
        selection.deleteFromDocument();
        selection.getRangeAt(0).insertNode(document.createTextNode(paste))
        event.preventDefault()
    })

    divEditor.addEventListener("keydown", function(event) {
        let keyCode = event.which || event.keyCode
        if (keyCode == 32) {
            document.execCommand("unlink", false, null)
            let sup = window.getSelection().focusNode.parentNode.nodeName
            if (sup === "SUP") {
                document.execCommand("superscript", false, null)
            }
            //console.log(window.getSelection())
        }
    })
}

let headingSeletor = document.querySelector("#heading")
headingSeletor.addEventListener("change", function() {
    let cmd = this.value
    document.execCommand("formatBlock", false, `<${cmd}>`)
    this.selectedIndex = 0
})


ToggleReference()

function ToggleReference() {
    let endNotes = document.querySelector("#end_notes")
    let addReference = document.querySelector("#addReference")
    endNotes.style.display = "none"
    addReference.addEventListener("click", () => {
        if (endNotes.style.display == "none") {
            endNotes.style.display = "block"
        } else {
            endNotes.style.display = "none"
        }
    })
}
setEndnotes()

function setEndnotes() {
    let compare = document.querySelector("#compare").innerHTML.toLowerCase()
    let addReference = document.querySelector("#addReference")
    let pretext = addReference.innerHTML
    let compareWith = "history"
    if (compare == compareWith) {
        addReference.innerHTML = ` ${pretext} End Notes`
    } else {
        addReference.innerHTML += `${pretext} References`
    }
}