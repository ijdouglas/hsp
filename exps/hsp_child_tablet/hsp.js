
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
    <p align="justify">You will watch a set of short videos and play a guessing game.
    Your task is to carefully watch the video and then guess the verb that was produced.</p>

    <p align="justify">Please keep in mind that the verbs you are asked to guess are all <b>concrete action verbs</b> such as "jump" and "clap".
    We are not asking you to guess abstract and general verbs like "think", "see/look", "do", or "make".
    Please enter correctly spelled <b>English</b> verbs in <b>present tense only</b>.</p>

    <p align="justify">Each video will only be played once, so make sure you pay close attention to the entire video.
    After the video, you have 40 seconds to enter your response.
    If you did not enter a valid answer after 40 seconds, the next trial will start. If you <b>miss 5 consecutive trials</b>, the study will automatically stop.</p>

    <p align="justify">The study session will last 20 min, please make sure you have enough time to finish the study in one session. There will be no breaks in between.</p>`,
    choices: ['Continue']
}


//////////////////
// Game slides //
////////////////

// sort images in the circle/area
var sorting_stimuli = []
for (var i = 0; i < 3; i++) {
    sorting_stimuli.push("images/sun.jpg")
    sorting_stimuli.push("images/moon.jpg")
}
var sorting_game = {
    type: 'free-sort',
    stimuli: sorting_stimuli,
    border_width: 10,
    prompt: '<p>Can you put <b>suns on the left side</b> and <b>moons on the right side?</b></p>',
    counter_text_unfinished: 'You still need to place %n% thing%s% inside the circle.',
    counter_text_finished: '<b>Good job! You did it!</b>'
}

// drag an image into the area
var drag_image_game = {
    type: 'free-sort',
    stimuli: ["images/fish.jpg"],
    sort_area_shape: "square",
    stim_height: 90,
    stim_width: 100,
    sort_area_height: 500,
    sort_area_width: 500,
    prompt: '<p>Can you drag the <b>fish</b> to the <b>upper right corner</b>?</p>',
    counter_text_unfinished: '',
    counter_text_finished: '<b>Good job! You did it!</b>'
}



///////////////////
// End of study //
/////////////////

var ask_name = {
    type: 'survey-html-form',
    preamble: 'What is your name?',
    html: '<input name="name" type="text" required="true" />'
}

var ask_age = {
    type: 'survey-html-form',
    preamble: 'Please indicate your age:',
    html: '<input name="age" type="number" required="true" />'
}

var ask_date = {
    type: 'survey-html-form',
    preamble: "Please select today's date:",
    html: '<input name="date" type="date" required="true" />'
}

var ask_ID = {
    type: 'survey-html-form',
    preamble: 'What is your ID?',
    html: '<input name="ID" type="number" required="true" />'
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



