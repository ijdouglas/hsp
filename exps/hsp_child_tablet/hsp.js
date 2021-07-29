
////////////////
// Variables //
//////////////

const attention_getter_count = 2 // this specifies the number of attention getting slides to show between each block

const video_order_file = "data/condition1.json" // json file should have the format {"videos": [.mp4 files], "block_location": [1,0,1,1,etc]}

// images for attention getting slides
const gameA_image1 = '<img src="images/butterfly1.jpg" width="150" height="100" border="0" alt="javascript button">'
const gameA_image2 = '<img src="images/butterfly2.jpg" width="150" height="100" border="0" alt="javascript button">'
const gameB_image1 = '<img src="images/flower1.jpg" width="100" height="130" border="0" alt="javascript button">'
const gameB_image2 = '<img src="images/flower2.jpg" width="100" height="130" border="0" alt="javascript button">'

/////////////////////////
// Instruction slides //
///////////////////////

var welcome = {
    type: 'html-button-response',
    stimulus: `<b>Welcome to the verb guessing game!</b><p>Press the button to begin</p>`,
    choices: ['Start']
}

var instructions = {
    type: 'html-button-response',
    stimulus: `<h1>Instructions</h1>
    <p align="justify">You will watch a set of short videos and play a guessing game.
    Your task is to carefully watch the video and then choose if the verb matches matches the video.</p>

    <p align="justify"> The video are split into 3 blocks with slides in-between, and each block has two video trials. </p>

    <p align="justify">Each video will only be played once, so make sure you pay close attention to the entire video.
    After the video, you have 40 seconds to enter your response. If you did not enter a valid answer after 40 seconds, the next trial will start.
    If you <b>miss 5 consecutive trials</b>, the study will automatically stop.</p>

    <p align="justify">The study session will last 20 min, please make sure you have enough time to finish the study in one session.
    There will be no breaks in between.</p>`,
    choices: ['Continue']
}

var start_videos = {
    type: 'html-button-response',
    stimulus: `<h2>Start of the experiment</h2><p>You will have 40 seconds to choose a response for each video.</p>`,
    choices: ['Start']
}

var finish_videos = {
    type: 'html-button-response',
    stimulus: `<p>You have finished the experiment! Please fill out the next few questions.</p>`,
    choices: ['Start']
}

var final_slide = {
    type: 'html-button-response',
    stimulus: '<b>That is the end of the study!</b><p>Thank you for participating!</p>',
    //prompt: '<i>Press the button to finish.</i>',
    choices: ['<b>Finish</b>']
}


//////////////////
// Intro Games //
////////////////

// Game 1: sort images in the circle/area
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

// Game 2: drag an image into the area
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


//////////////////////////////////////
// Attention getter + Video trials //
////////////////////////////////////

var video_trial_timeline = [] // timeline for video trials & attention getting slides

// variables for attention getter
var image1 = ''
var image2 = ''
var alternateImages = false

// attention getter
var spot_different_image_game = {
    type: 'html-button-response',
    stimulus: '<h3>Can you choose the one that is different?</h3>',
    choices: ['-', '-', '-', '-', '-'],
    button_html: function () {
        if (alternateImages == false) {
            image1 = gameA_image1
            image2 = gameA_image2
        } else {
            image1 = gameB_image1
            image2 = gameB_image2
        }
        alternateImages = !alternateImages

        // create array of identical image objects for game
        var image_array = [image1, image1, image1, image1, image1]

        // randomly choose an image to be different
        var random_num = Math.floor(Math.random() * image_array.length)
        image_array[random_num] = image2
        return image_array
    }
}

// add video trials and insert attention getters (using json file with video orders)
fetch(video_order_file)
    .then(res => res.json())
    .then(data => {

        var stimuli_set = data["videos"]            // gather videos for the experiment
        var block_location = data["block_location"] // gather block numbers assigned to each video

        for (var i = 0; i < stimuli_set.length; i++) {

            // add attention getter at the start of a new block
            if (block_location[i] == 1) {
                for (var j = 0; j < attention_getter_count; j++)
                    video_trial_timeline.push(spot_different_image_game)
            }

            // video trials
            var video_trial = {
                type: 'video-button-response',
                stimulus: [stimuli_set[i]],
                choices: ['smile', 'frown'],
                button_html: [
                    '<img src="images/smile.jpg" width="110" height="110" border="0" alt="javascript button">',
                    '<img src="images/frown.jpg" width="110" height="110" border="0" alt="javascript button">'],
                width: 550,
                trial_duration: 40000,
                //response_allowed_while_playing: false,
                on_finish: function (data) {
                    if (data.response == 0)
                        data.answer = 'smile'
                    else if (data.response == 1)
                        data.answer = 'frown'
                    else
                        data.answer = 'no answer'
                }
            }

            video_trial_timeline.push(video_trial)
        } // end of for-loop

    })

////////////////
// Questions //
//////////////

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


////////////////
// Functions //
//////////////

// get file name from file path
function baseName(str) {
    var base = new String(str).substring(str.lastIndexOf('/') + 1);
    if (base.lastIndexOf(".") != -1)
        base = base.substring(0, base.lastIndexOf("."));
    return base;
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



