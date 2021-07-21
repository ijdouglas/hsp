
//////////////////////////////////////
// Instruction & transition slides //
////////////////////////////////////

var welcome = {
    type: 'html-button-response',
    stimulus: `<b>Welcome to the verb guessing game!</b><p>Press the button to begin</p>`,
    choices: ['Start']
}

var instructions = {
    type: 'html-button-response',
    stimulus: `<h1>Instructions</h1>
    <p align="justify">You will watch a set of short videos recorded during a parent-child play session and play a guessing game.
    Each of these videos is extracted from the moment when parent mentioned an action verb in toy play. The actual verb parent said is replaced by an artificial word.
    Your task is to carefully watch the video and then guess the verb that parents produced at the moment, indicated by the artificial word.</p>
    
    <p align="justify">Please keep in mind that the verbs you are asked to guess are all <b>concrete action verbs</b> such as "jump" and "clap".
    We are not asking you to guess abstract and general verbs like "think", "see/look", "do", or "make".
    Please enter correctly spelled <b>English</b> verbs in <b>present tense only</b>.</p>

    <p align="justify">Each video will only be played once, so make sure you pay close attention to the entire video and only start typing the answer after the video.
    After the video, you have 40 seconds to enter your response. If you are unsure or do not know, please still try to provide your best guess within 40 seconds.
    If you did not enter a valid answer after 40 seconds, the next trial will start. If you <b>miss 5 consecutive trials</b>, the study will automatically stop.</p>

    <p align="justify">The study session will last 20 min, please make sure you have enough time to finish the study in one session. There will be no breaks in between.</p>`,
    choices: ['Continue']
}



///////////////////
// End of study //
/////////////////

var ask_name = {
    type: 'survey-html-form',
    preamble: 'What is your name?',
    html: '<input name="name" type="text" />'
}

var ask_age = {
    type: 'survey-html-form',
    preamble: 'Please indicate your age:',
    html: '<input name="age" type="number" />'
}

var ask_date = {
    type: 'survey-html-form',
    preamble: "Please select today's date:",
    html: '<input name="date" type="date" />'
}

var ask_ID = {
    type: 'survey-html-form',
    preamble: 'What is your ID?',
    html: '<input name="ID" type="number" />'
}


// end slide
var end_slide = {
    type: 'html-button-response',
    stimulus: `<b>That is the end of the study!</b><p>Thank you for participating!</p>`,
    choices: ['Finish']
}

////////////////
// Functions //
//////////////

// shuffle an array's elements
function shuffle(array) {
    return shuffle(array, 0, array.length - 1);
}

// shuffle an array's elements within specified range (inclusive)
function shuffle(array, startIndex, endIndex) {
    for (let i = endIndex; i > startIndex; i--) {
        const j = Math.floor(Math.random() * i)
        const temp = array[i]
        array[i] = array[j]
        array[j] = temp
    }
    return array;
}

// get file name from file path
function baseName(str) {
    var base = new String(str).substring(str.lastIndexOf('/') + 1);
    if (base.lastIndexOf(".") != -1)
        base = base.substring(0, base.lastIndexOf("."));
    return base;
}

// check if response is not empty
function validate_response(resp) {
    if (resp.length > 0)
        return true;
    else
        return false;
}

function reqListener() {
    console.log(this.responseText);
}

// save experiment data as csv
function saveData(name, data) {
    console.log("trying to save data")
    jsPsych.data.addProperties({ subject: ID });
    var xhr = new XMLHttpRequest();
    xhr.addEventListener("load", reqListener);
    xhr.open('POST', 'write_data.php');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ filename: name, filedata: data }));
}



