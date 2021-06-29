var transitionDelay = 100;

// original code from experiment pasted below -------------------------------------------------
/*
var normalpause = 1500;

// show slide function
function showSlide(id) {
    $(".slide").hide(); //jquery - all elements with class of slide - hide
    $("#" + id).show(); //jquery - element with given id - show
}

createDot = function (dotx, doty, i, tag) {
    var dots;
    if (tag === "smiley") {
        dots = ["smiley1", "smiley2", "smiley3", "smiley4", "smiley5"];
    } else {
        dots = [1, 2, 3, 4, 5];
    }

    var dot = document.createElement("img");
    dot.setAttribute("class", "dot");
    dot.id = "dot_" + dots[i];
    if (tag === "smiley") {
        dot.src = "dots/dot_" + "smiley" + ".jpg";
    } else {
        dot.src = "dots/dot_" + dots[i] + ".jpg";
    }

    var x = Math.floor(Math.random() * 950);
    var y = Math.floor(Math.random() * 540);

    var invalid = "true";

    //make sure dots do not overlap
    while (true) {
        invalid = "true";
        for (j = 0; j < dotx.length; j++) {
            if (Math.abs(dotx[j] - x) + Math.abs(doty[j] - y) < 250) {
                var invalid = "false";
                break;
            }
        }
        if (invalid === "true") {
            dotx.push(x);
            doty.push(y);
            break;
        }
        x = Math.floor(Math.random() * 400);
        y = Math.floor(Math.random() * 400);
    }

    dot.setAttribute("style", "position:absolute;left:" + x + "px;top:" + y + "px;");
    training.appendChild(dot);
}


//for critical trials and fillers
var images = new Array();
for (i = 0; i < allimages.length; i++) {
    images[i] = new Image();
    images[i].src = "tabletobjects/" + allimages[i] + ".jpg";
}

//for dot game
var dots = ["dot_1", "dot_2", "dot_3", "dot_4", "dot_5", "x", "dot_smiley"];
for (i = 0; i < dots.length; i++) {
    images[i] = new Image();
    images[i].src = "dots/" + dots[i] + ".jpg";
}



var experiment = {

    //sets up and allows participants to play "the dot game"
    training: function (dotgame) {
        var allDots = ["dot_1", "dot_2", "dot_3", "dot_4", "dot_5",
            "dot_smiley1", "dot_smiley2", "dot_smiley3",
            "dot_smiley4", "dot_smiley5"];
        var xcounter = 0;
        var dotCount = 5;

        //preload sound
        if (dotgame === 0) {
            audioSprite.play();
            audioSprite.pause();
        }

        var dotx = [];
        var doty = [];

        if (dotgame === 0) {
            for (i = 0; i < dotCount; i++) {
                createDot(dotx, doty, i, "");
            }
        } else {
            for (i = 0; i < dotCount; i++) {
                createDot(dotx, doty, i, "smiley");
            }
        }
        showSlide("training");
        $('.dot').bind('click touchstart', function (event) {
            var dotID = $(event.currentTarget).attr('id');

            //only count towards completion clicks on dots that have not yet been clicked
            if (allDots.indexOf(dotID) === -1) {
                return;
            }
            allDots.splice(allDots.indexOf(dotID), 1);
            document.getElementById(dotID).src = "dots/x.jpg";
            xcounter++
            if (xcounter === dotCount) {
                setTimeout(function () {
                    $("#training").hide();
                    if (dotgame === 0) {
                        //hide old x marks before game begins again
                        var dotID;
                        for (i = 1; i <= dotCount; i++) {
                            dotID = "dot_" + i;
                            training.removeChild(document.getElementById(dotID));
                        }
                        experiment.training();
                        dotgame++;
                    } else {
                        //document.body.style.background = "black";
                        setTimeout(function () {
                            //showSlide("prestudy");
                            //experiment.next();
                        }, normalpause * 2);
                    }
                }, normalpause * 2);
            }
        });
    }
}
*/


//////////////////////////////////////
// Instruction & transition slides //
////////////////////////////////////

var welcome = {
    type: 'html-button-response',
    stimulus: `Welcome to the verb guessing game!<p>Press the button to begin</p>`,
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

    <p align="justify"> Please provide your top 3 guesses with the first choice being the most likely verb, the second choice being the next possible verb,
    and the third choice being the third most likely verb. You are allowed to choose the same verb more than once if you are certain that that verb is correct. </p>
    <p align="justify">For example, you could guess "eat", "bite", "chew" for a trial if you think all three guesses are all likely to be correct,
    or you could guess "eat","eat","bite" if you think "eat" is more likely to be correct than "bite", or you could guess "eat", "eat", "eat"
    if you think the correct verb is definitely eat. You have to provide 3 guesses in order to proceed.</p>

    <p align="justify">Each video will only be played once, so make sure you pay close attention to the entire video and only start typing the answer after the video.
    After the video, you have 40 seconds to enter your response. If you are unsure or do not know, please still try to provide your best guess within 40 seconds.
    If you did not enter a valid answer after 40 seconds, the next trial will start. If you <b>miss 5 consecutive trials</b>, the study will automatically stop.</p>

    <p align="justify">The study session will last 20 min, please make sure you have enough time to finish the study in one session. There will be no breaks in between.</p>
    <p>Let's do a sound check on the next page!</p>`,
    choices: ['Continue']
}

// training trials instructions
var instruction_training = {
    type: 'html-button-response',
    stimulus: `<h1>Examples</h1>
        <p align="justify">Now you will see 1 example video. Please provide 3 guesses the parent in the video is saying by entering the verb in the boxes below the video. You will see the correct answer afterwards.  
        </p>Again, please keep in mind:<br>
        <li>Verbs you are asked to guess are all <b>concrete action verbs (e.g. jump, clap)</b></li>
        <li>Enter only <b>English verbs in present tense</b></li>
        <li>For example trials, you have <b>60 seconds</b> to enter your response.</li>
        <li>Provide your top 3 guesses even if you are unsure</li>
        <li>You are allowed to repeat the same guess multiple times (2 or 3 times) if you are certain about that guess</li>
        <p>Example trials will start on the next page.</p>
        <p>Press the button to proceed</p>`,
    choices: ['Start']
}

// end of training trials
var end_training = {
    type: 'html-button-response',
    stimulus: `
        <p>That's all the training examples. Now you will begin guessing on your own.</p>
        <p>Press the button to continue</p>`,
    choices: ['Continue']
};

// experiment trials instructions 
var instruction_experiment = {
    type: 'html-button-response',
    stimulus: `<h1>Start Experiment</h1>
        <p align="center">Now we will start the real experimental trials.</p>
        <p>You will see 1 block of trials, each block consists of 2 trials. <b>Parent in each block is naming the SAME verb</b>, your job is to guess which verb parent is naming right after watching each trial.</p>
        <p>Throughout the trials within a block, you can change your guess at any given trial. However, if you believe your previous answers are correct, you can choose the same answers again. You are not allowed to go back and change your previous answers and <b>no feedback will be provided from now on</b>.</p>  
        <p>You will start the real experiment on the next page.</p>
        <p>Press the button to proceed</p>`,
    choices: ['Start']
}

// start of new block of experiment trials
var start_new_block = {
    type: 'html-button-response',
    stimulus: `
        <p>Beginning of a new block</p>
        <p>Please guess a new verb</p>
        <p><b>Parent in this block is naming the SAME verb</b></p>
        <p>Press the button to continue</p>`,
    choices: ['Continue']
}


///////////////////
// End of study //
/////////////////

var sex_demographic = {
    type: 'survey-multi-choice',
    questions: [    // array of questions
        {
            prompt: "<b>Demographic Report</b><p>Please indicate your sex:",    // question/prompt
            name: 'Sex',                                                        // name for storing data
            options: ['Male', 'Female', 'Other', 'I decline to respond'],       // answer choices
            required: true,                                                     // response required
            horizontal: true                                                    // horizontal options
        }
    ]
}

var age_demographic = {
    type: 'survey-html-form',
    preamble: 'Please indicate your age:',
    html: '<input name="age" type="text" />'
}

var language_demographic = {
    type: 'survey-html-form',
    preamble: 'Are you a native English speaker? If not, please enter your native language and how long you have been learning English:',
    html: '<input name="Language" type="text" />'
}

var other_demographic = {
    type: 'survey-multi-choice',
    questions: [    // array of 3 multiple choice questions
        {
            prompt: "Please indicate your ethnicity:",
            name: 'Ethnicity',
            options: ['Hispanic or Latino', 'Not Hispanic or Latino', 'I decline to Respond'],
            required: true,
            horizontal: true
        },
        {
            prompt: "Please indicate your race:",
            name: 'Race',
            options: ['American Indian or Alaskan Native', 'Asian', 'Black or African American', 'Native Hawaiian or Pacific Islander', 'White', 'I decline to respond'],
            required: true,
            horizontal: true
        },
        {
            prompt: "What is your highest level of education?",
            name: 'Education',
            options: ['Never finished high school or GED', 'High school diploma or GED, but no college coursework', 'Some college, but have not completed a post-secondary degree', 'Associate\'s degree', 'Bachelor\'s degree', 'Bachelor\'s degree and some graduate/professional coursework', 'Completed a graduate or professional degree'],
            required: true,
            horizontal: true
        }
    ]
}

/*
var ask_name = {
    type: 'survey-text',
    questions: [
        { prompt: "What is your name?" }
    ],
};

var form_survey_reminder = {
    type: 'html-keyboard-response',
    stimulus: "Please go back to the google form survey and complete PART 2"
};

var secret_word = {
    type: 'html-keyboard-response',
    stimulus: "Remember or write down the word \"<b>IU200</b>\". <p><b>You will be asked to enter this word in the google form survey.</p></b>"
};
*/
/*
var completion_code = [`Remember or write down the completion code: IU200<p><b>You will be asked to enter this code in MTurk.</p></b>`];

var completion_code_turk = [`<p>Thank you for your participation!</p> To help us process your payment, please write down or remember this code: <b>IU200</b><p><b>You will need to enter this code in Amazon.</p></b>`];

var end = [`That's all the videos. Thank you for participating! You can close this this page now, data will be automatically save`];

var end_turk = [`<p>Your data are automatically saved, please close this web page now. </p> <p>If you have not done so, please write down or remember this code: <b>IU200</b></p>Then enter it back in Amazon.`];


// end of study instructions
var end_block = {
    type: "instructions",
    pages: [completion_code, end],
    show_clickable_nav: true,
    timing_post_trial: transitionDelay
};
// end of study instructions (turk)
var end_block_turk = {
    type: "instructions",
    pages: [completion_code_turk, end_turk],
    show_clickable_nav: true,
    timing_post_trial: transitionDelay
};
*/

// end slide (temporary)
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

////////////////////
// Custom plugin // -- video trial with free response
//////////////////
jsPsych.plugins['hsp-free-response'] = (function () {

    var plugin = {};

    plugin.info = {
        name: 'hsp-free-response',

        parameters: {
            sources: {
                type: jsPsych.plugins.parameterType.VIDEO,
                pretty_name: 'Video',
                default: undefined,
                description: 'The video file to play.'
            },
            trial_duration: {
                type: jsPsych.plugins.parameterType.INT,
                pretty_name: 'Trial duration',
                default: null,
                description: 'The maximum duration to wait for a response.'
            },
            num_responses: {
                type: jsPsych.plugins.parameterType.INT,
                pretty_name: 'NumResponses',
                default: '',
                description: 'The number of responses fields available to subject.'
            },
            width: {
                type: jsPsych.plugins.parameterType.INT,
                pretty_name: 'Width',
                default: '',
                description: 'The width of the video in pixels.'
            },
            height: {
                type: jsPsych.plugins.parameterType.INT,
                pretty_name: 'Height',
                default: '',
                description: 'The height of the video display in pixels.'
            },
            autoplay: {
                type: jsPsych.plugins.parameterType.BOOL,
                pretty_name: 'Autoplay',
                default: true,
                description: 'If true, the video will begin playing as soon as it has loaded.'
            },
            controls: {
                type: jsPsych.plugins.parameterType.BOOL,
                pretty_name: 'Controls',
                default: false,
                description: 'If true, the subject will be able to pause the video or move the playback to any point in the video.'
            },
            questions: {
                type: jsPsych.plugins.parameterType.COMPLEX,
                array: true,
                pretty_name: 'Questions',
                default: undefined,
                nested: {
                    prompt: {
                        type: jsPsych.plugins.parameterType.STRING,
                        pretty_name: 'Prompt',
                        default: undefined,
                        description: 'Prompt for the subject to response'
                    },
                    placeholder: {
                        type: jsPsych.plugins.parameterType.STRING,
                        pretty_name: 'Value',
                        default: "",
                        description: 'Placeholder text in the textfield.'
                    },
                    rows: {
                        type: jsPsych.plugins.parameterType.INT,
                        pretty_name: 'Rows',
                        default: 1,
                        description: 'The number of rows for the response text box.'
                    },
                    columns: {
                        type: jsPsych.plugins.parameterType.INT,
                        pretty_name: 'Columns',
                        default: 40,
                        description: 'The number of columns for the response text box.'
                    },
                    required: {
                        type: jsPsych.plugins.parameterType.BOOL,
                        pretty_name: 'Required',
                        default: false,
                        description: 'Require a response'
                    },
                    name: {
                        type: jsPsych.plugins.parameterType.STRING,
                        pretty_name: 'Question Name',
                        default: '',
                        description: 'Controls the name of data values associated with this question'
                    }
                }
            },
            preamble: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'Preamble',
                default: null,
                description: 'HTML formatted string to display at the top of the page above all the questions.'
            },
            button_label: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'Button label',
                default: 'Continue',
                description: 'The text that appears on the button to finish the trial.'
            }
        }
    }

    plugin.trial = function (display_element, trial) {

        jsPsych.pluginAPI.clearAllTimeouts();

        console.log(`trial duration:  ${trial.trial_duration}`)

        /*****************************************
            Setup for video playback element
        ******************************************/
        html = ''
        html += '<div>'
        html += '<video id="jspsych-video-keyboard-response-stimulus"';

        if (trial.width) {
            html += ' width="' + trial.width + '"';
        }
        if (trial.height) {
            html += ' height="' + trial.height + '"';
        }
        if (trial.autoplay) {
            html += " autoplay ";
        }
        if (trial.controls) {
            html += " controls ";
        }
        html += ">";

        var video_preload_blob = jsPsych.pluginAPI.getVideoBuffer(trial.sources[0]);
        if (!video_preload_blob) {
            for (var i = 0; i < trial.sources.length; i++) {
                var file_name = trial.sources[i];
                if (file_name.indexOf('?') > -1) {
                    file_name = file_name.substring(0, file_name.indexOf('?'));
                }
                var type = file_name.substr(file_name.lastIndexOf('.') + 1);
                type = type.toLowerCase();
                html += '<source src="' + file_name + '" type="video/' + type + '">';
            }
        }
        html += "</video>";
        html += "</div>";


        /*****************************************
            Setup for text response elements
        ******************************************/

        if (typeof trial.question.rows == 'undefined') {
            trial.question.rows = 1;
        }

        if (typeof trial.question.columns == 'undefined') {
            trial.question.columns = 40;
        }

        if (typeof trial.question.value == 'undefined') {
            trial.question.value = "";
        }

        if (trial.preamble !== null) {
            html += '<div id="jspsych-survey-text-preamble" class="jspsych-survey-text-preamble">' + trial.preamble + '</div>';
        }
        // start form
        html += '<form id="jspsych-survey-text-form">'

        q = trial.question

        html += '<div id="jspsych-survey-text-' + 1 + '" class="jspsych-survey-text-question" style="margin: 2em 0em;">';
        html += '<p class="jspsych-survey-text">' + q.prompt + '</p>';

        for (var i = 0; i < trial.num_responses; i++) {
            var autofocus = i == 0 ? "autofocus" : "";
            var req = q.required ? "required" : "";
            html += '<input type="text" autocomplete="off" id="input-' + i + '"  name="#jspsych-survey-text-response-' + i + '" data-name="' + q.name + '" size="' + q.columns + '" ' + autofocus + ' ' + req + ' placeholder="' + q.placeholder + '" disabled></input><br>';
        }


        // add submit button
        html += '<input type="submit" id="jspsych-survey-text-next" class="jspsych-btn jspsych-survey-text" value="' + trial.button_label + '"></input>';

        html += '</form>'

        display_element.innerHTML = html;


        var end_trial = function () {
            var endTime = performance.now();
            var response_time = endTime - startTime;

            // kill any remaining setTimeout handlers
            jsPsych.pluginAPI.clearAllTimeouts();

            // kill keyboard listeners
            if (typeof keyboardListener !== 'undefined') {
                jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
            }

            var data = {
                video: file_name,
                words: []
            };

            console.log("hello from end_trial")

            for (var index = 0; index < trial.num_responses; index++) {
                var response = document.querySelector('#input-' + index).value;
                data.words.push(response)
            }

            // save data
            var trial_data = {
                "rt": response_time,
                "response": JSON.stringify(data)
            };

            // clear the display
            display_element.innerHTML = '';

            // move on to the next trial
            jsPsych.finishTrial(trial_data);
        };

        // activate textbox
        display_element.querySelector('#jspsych-video-keyboard-response-stimulus').addEventListener('ended', function activateTextbox(e) {
            document.getElementById("input-0").removeAttribute("disabled");
            document.getElementById("input-1").removeAttribute("disabled");
            document.getElementById("input-2").removeAttribute("disabled");
        });


        display_element.querySelector('#jspsych-survey-text-form').addEventListener('submit', function (e) {
            e.preventDefault();
            // measure response time
            var endTime = performance.now();
            var response_time = endTime - startTime;

            jsPsych.pluginAPI.clearAllTimeouts();

            // create object to hold responses
            var data = {
                video: file_name,
                words: []
            };

            var valid = true;

            for (var index = 0; index < trial.num_responses; index++) {
                var response = document.querySelector('#input-' + index).value;
                // if (!validate_response(response)) {
                //     valid = false;
                // }
                if (response === "") {
                    return
                }
                data.words.push(response)
            }

            // save data
            var trialdata = {
                "rt": response_time,
                "response": JSON.stringify(data)
            };

            display_element.innerHTML = '';

            // next trial
            if (valid) {
                jsPsych.finishTrial(trialdata);
            } else {
                console.log("something is wrong")
                return;
            }
        });
        var startTime = performance.now();


        if (trial.trial_duration !== null) {
            jsPsych.pluginAPI.setTimeout(function () {
                end_trial();
            }, trial.trial_duration);
        }
    }
    return plugin;
})();


