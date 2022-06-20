
/*  NOTES for data recorded in the study:
 *  - �answer� records the responses: 1 = smile, 0 = frown
 *  - �response� is the opposite of �answer� and can be ignored since the jsPsych plugins automatically makes it store the spot of the answer chosen (0 = first answer, 1 = second answer, etc)
 *  - �accuracy� is the correctness of each answer: 1 = correct, 0 = incorrect
 *  - �verb� is the verb executed in the video
 */

////////////////
// Variables //
//////////////

// file - specifies video order and blocks
/* INSTRUCTIONS for block location:
 * - 2 = start of a new block of training videos; 1 = start of testing videos; and, 0 = other.
 * - The 0th index should be 0 even though it is the start of a block of training videos
 * - Example: [0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 1, 0, 0] is 2 blocks of 4 training videos, then 3 testing videos
 */
const video_json_file = "data/condition.json" // json file should have the format {"videos": [.mp4 files], "block_location": [2,0,0,1,0,0,etc]}

// this specifies the number of attention getting slides to show between each block
const attention_getter_count = 2 


// image html for attention getters (alternates between game A and game B images)
const gameA_image1 = '<img src="data/images/butterfly1.jpg" width="150" height="100" border="0" alt="javascript button">'
const gameA_image2 = '<img src="data/images/butterfly2.jpg" width="150" height="100" border="0" alt="javascript button">'
const gameB_image1 = '<img src="data/images/flower1.jpg" width="100" height="130" border="0" alt="javascript button">'
const gameB_image2 = '<img src="data/images/flower2.jpg" width="100" height="130" border="0" alt="javascript button">'

// image html for video trials
const a_option = '<img src="data/images/image_a_option.jpg" width="50" height="50" border="0" alt="javascript button">'
const b_option = '<img src="data/images/image_b_option.jpg" width="50" height="50" border="0" alt="javascript button">'
const both_option = '<img src="data/images/image_both_option.jpg" width="75" height="40" border="0" alt="javascript button">'
const neither_option = '<img src="data/images/image_neither_option.jpg" width="100" height="40" border="0" alt="javascript button">'

/////////////////////////
// Instruction slides //
///////////////////////

var enter_fullscreen = {
    type: 'fullscreen',
    fullscreen_mode: true,
    delay_after: 0,
    message: '<p>The experiment will be in full screen mode. Please press the button below</p>'
}

var exit_fullscreen = {
    type: 'fullscreen',
    fullscreen_mode: false
}

// first welcoming slide
var welcome = {
    type: 'html-button-response',
    stimulus: `<img src="data/images/dog_waving.png" height="200">
               <h2>Welcome to the verb guessing game!</h2>
               <p>Press the button to begin</p>`,
    choices: ['Begin']
}

// instructions at the beginning of the experiment
var instructions = {
    type: 'html-button-response',
    stimulus: `<h1>Instructions</h1>
    <p align="justify">You will watch a set of short videos and be tested on what you learned.</p>

    <p align="justify">The video are split into blocks with attention-getting slides in-between.</p>

    <p align="justify">Each video will only be played once, so make sure you pay close attention to the entire video.
    After the video, you have 40 seconds to enter your response. If you did not enter a valid answer after 40 seconds, the next trial will start.`,
    choices: ['Continue']
}

// start of video trials
var start_videos = {
    type: 'html-button-response',
    stimulus: `<h2>Let's start watching the videos!</h2>
               <p>You will hear a word during every video, please make sure your volume is turned up before starting.</p>`,
    choices: ['Start']
}

// start of new block of video trials
var start_new_block = {
    type: 'html-button-response',
    stimulus: "<h4>Let's learn another word, ready?</h4>",
    choices: ['Ready!']
}

// start of testing videos in a block
var start_testing_videos = {
    type: 'html-button-response',
    stimulus: `Now you will see some videos one at a time.
               <p>Select the answer choice for the word you see represented in the video.<p>`,
    choices: ['Continue']
}

// end of video trials
var finish_videos = {
    type: 'html-button-response',
    stimulus: `<p>You are done! Please fill out the next few questions.</p>`,
    choices: ['Next']
}

// final slide that ends the experiment
var final_slide = {
    type: 'html-button-response',
    stimulus: `<img src="data/images/bye_image.jpg" height="200">
               <h3>All done!</h3><p>Good job! Press the button to finish.</p>`,
    choices: ['<b>Finish</b>']
}


//////////////////
// Intro Games //
////////////////

// Game 1: sort images in the circle/area
var sorting_stimuli = []
for (var i = 0; i < 2; i++) {
    sorting_stimuli.push("data/images/sun.jpg")
    sorting_stimuli.push("data/images/moon.jpg")
}
var sorting_game = {
    type: 'free-sort',
    stimuli: sorting_stimuli,
    sort_area_shape: "square",
    border_width: 9,       // width of the border of the sort area
    stim_height: 90,       // height of the stimuli images
    stim_width: 90,        // width of the stimuli images
    sort_area_height: 400, // height of the area that the stimuli can be moved into
    sort_area_width: 600,  // width of the area that the stimuli can be moved into
    prompt: `<b>Can you put all the suns and moons inside the rectangle?</b>
             <p>Try to put the suns on the left and the moons on the right.</p>`,
    counter_text_unfinished: '<i>You still need to place %n% thing%s% inside the circle.</i>',
    counter_text_finished: '<b>Good job! You did it!</b>',
    column_spread_factor: .6 // how far away the items are placed from the sorting area
}

// Game 2: drag an image into the area
var drag_image_game = {
    type: 'free-sort',
    stimuli: ["data/images/fish.jpg"],
    sort_area_shape: "square",
    stim_height: 90,        // height of the stimuli images
    stim_width: 100,        // width of the stimuli images
    sort_area_height: 300,  // height of the area that the stimuli can be moved into
    sort_area_width: 400,   // width of the area that the stimuli can be moved into
    prompt: `<b>Can you move the fish inside the rectangle?</b>
             <p>Try to put it at the upper right corner of the rectangle.</p>`,
    counter_text_unfinished: '',
    counter_text_finished: '<b>Good job! You did it!</b>'
}


//////////////////////////////////////
// Attention getter + Video trials //
////////////////////////////////////

var video_trial_timeline = [] // timeline for video trials & attention getting slides

// variables for attention getter plugin (leave it as it is)
var image1 = ''
var image2 = ''
var alternateImages = false

// attention getter
var spot_different_image_game = {
    type: 'html-button-response',
    stimulus: '<h3>Can you find the one that is different?</h3>',
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
fetch(video_json_file)
    .then(res => res.json())
    .then(data => {

        var stimuli_set = data["videos"]            // gather videos for the experiment
        var block_location = data["block_location"] // gather block numbers assigned to each video

        var current_block = [] // contains the current block of video trials (either training or testing)
        var isTrainingVideo = true
        var training_block_verb = " " // verb of the current training block

        for (var i = 0; i < stimuli_set.length; i++) {

            // add attention getter at the start of a new block
            if (block_location[i] == 2) {
                for (var j = 0; j < attention_getter_count; j++)
                    video_trial_timeline.push(spot_different_image_game)

                video_trial_timeline.push(start_new_block)
                isTrainingVideo = true
            }

            if (block_location[i] == 1) {
                isTrainingVideo = false
            }

            // get verb from video file name
            var file_name = baseName(stimuli_set[i])
            var verb = file_name.split("_")[1]

            if (isTrainingVideo) { 
                training_block_verb = verb

                // plugin for training videos
                var training_video = {
                    type: 'video-button-response',
                    stimulus: [stimuli_set[i]],
                    choices: [''],
                    button_html: '<img src="data/images/transparent_image.png" width="5" height="5" border="0" alt="javascript button">',
                    width: 550,
                    trial_ends_after_video: true,
                    response_allowed_while_playing: false,
                    data: { verb: verb },
                    post_trial_gap: 500
                }
                current_block.push(training_video)

            } else { 
                // plugin for testing videos
                var testing_video = {
                    type: 'video-button-response',
                    stimulus: [stimuli_set[i]],
                    prompt: "Is this the same verb?",
                    choices: ['a', 'b', 'both', 'neither'],
                    button_html: [a_option, b_option, both_option, neither_option],
                    width: 550,
                    trial_duration: 40000,
                    response_allowed_while_playing: false,
                    data: {
                        verb: verb,
                        training_block_verb: training_block_verb
                    },
                    on_finish: function (data) {
                        // record answer in data
                        if (data.response == 0)
                            data.answer = 1 // happy face
                        else {
                            if (data.response == 1)
                                data.answer = 0 // sad face
                            else
                                data.answer = -1 // did not answer before time ran out
                        }

                        // record answer accuracy in data
                        if (data.verb === data.training_block_verb && data.answer == 1 ||
                            data.verb !== data.training_block_verb && data.answer == 0)
                            data.accuracy = 1
                        else
                            data.accuracy = 0
                    }
                }
                current_block.push(testing_video)

            } // end of if-else statement

            // if reached end of block for training or testing, randomize videos and add to timeline
            if (i + 1 >= stimuli_set.length || block_location[i + 1] > 0) {
                current_block = shuffle(current_block)

                // insert testing video instructions slide before testing videos
                if (!isTrainingVideo)
                    video_trial_timeline.push(start_testing_videos)

                current_block.forEach(element => video_trial_timeline.push(element)) // add shuffled video slides to timeline
                current_block = []
            }

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

// shuffle an array's elements
function shuffle(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1))
        var temp = array[i]
        array[i] = array[j]
        array[j] = temp
    }
    return array
}

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



