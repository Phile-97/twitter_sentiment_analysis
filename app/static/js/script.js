// Scripts to be executed in the browser
var tags = []

// search keywords in the database
function search(id, list) {
    text = document.getElementById(id).value;
    fetch('/search', {
        method: 'post',
        body: JSON.stringify({'type':id, 'keyword': text}),
        headers: {"Content-type": "application/json; charset=UTF-8"},
    })
    .then(response => response.json()) 
    .then(json => update_list(json, list))
    .catch(err => console.log(err))
}


// Autocomplete
function update_list(obj, lst) {
    let arr = JSON.parse(obj['data'])
    lst.innerHTML = ''
    if (arr.length > 0) {
        arr.forEach(ele => {
            lst.innerHTML += `
            <option onselect="add_tag()">${ele}</option>
            `
        })
    }
}


// add tags
function add_tag(val, lst) {
    let options = lst.options
    for(let i=0; i<options.length;i++) {
        if(options[i].value === val && !tags.includes(val)) {
            tags.push(val)
            document.getElementById('keywords').innerHTML += `
                <input type='button' class='btn btn-sm btn-outline-secondary btn-light mr-1 text-dark' value=${val} onclick='rem_tag(this)'>
            `
        }
    }
    // update value
    document.getElementById('tags').value = tags.toString();
}

// remove tags
function rem_tag(ele) {
    let idx = tags.indexOf(ele.value)
    if (idx > -1) {
        tags.splice(idx, 1)
    }
    ele.remove()

    // update value
    document.getElementById('tags').value = tags.toString();
}

// show/hide tweets
function show(s) {
    let tweets = document.getElementsByClassName('tweepy');
    let sentiment = document.getElementsByClassName(s);

    for (let i = 0; i < tweets.length; i++) {
        tweets[i].classList.add('hidden');
    }
    
    for (let i = 0; i < sentiment.length; i++) {
        sentiment[i].classList.remove('hidden');
    }

    location.href = '#tweets_box'
}


// generate pdf
function generate_pdf() {
    var doc = new jsPDF('p', 'pt')
    var header = function (data) {
        doc.setFontSize(18);
        doc.setTextColor(40);
        doc.setFontStyle('normal');
//doc.addImage(headerImgData, 'JPEG', data.settings.margin.left, 20, 50, 50);
        doc.text("Sentiment Analysis Report", data.settings.margin.left+250, 50, 'center');
    };
    doc.autoTable({ html: '#mytable',
                    theme: 'grid',
                    columnStyles: {
                        0: {overflow: 'linebreak'}
                    },
                    margins: {top: 80},
                    beforePageContent: header
                });
    doc.save('tweets.pdf')
}