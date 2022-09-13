
// var consent = [`
// <p align="left">MTurk2</p>

// <p align="left">Study #0808000094</p>

// <p align="left"><b>Indiana University</b></p>
// <p align="left"><b>INFORMED CONSENT STATEMENT</b></p>
// <p align="left"><b>Multimodal Word Learning – Cross-Situational Learning in Adults</b></p>
// <p align="left">You are invited to participate in a research study of language learning. We are interested
// in how people learn words and categories. We are mainly concerned with how humans
// learn to associate words with referents. We are not interested in the particular behaviors
// of particular individuals.</p>

// <p align="left"><b>INFORMATION</b></p>

// <p align="left">The entire study will last 20 minutes. You will be asked to study some videos/pictures
// while listening to some sounds/words. You may be asked to learn which sound/word
// goes with which referent in the visual stimuli. During or after this experiment, your
// performance will be automatically collected. These data help us assess learning over the
// course of the experiment.</p>

// <p align="left"><b>RISKS</b></p>

// <p align="left">There is potential risk of loss of confidentiality. This risk is minimized by the investigator,
// as outlined in the confidentiality section.</p>

// <p align="left"><b>BENEFITS</b></p>

// <p align="left">There are no direct benefits to the subjects. However, the findings will give us more
// information about how people link words to object categories.</p>

// <p align="left"><b>NUMBER OF PEOPLE TAKING PART IN THE STUDY</b></p>

// <p align="left">If you agree to participate, you will be one of approximately 1,500 people who will be
// participating in this research study.</p>

// <p align="left"><b>CONFIDENTIALITY</b></p>

// <p align="left">Your identity will be held in confidence in reports in which the study may be
// published. The digital record and data will be saved on a password-protected computer
// in a locked laboratory. The data collected from you will be made available only to
// trained experimenters conducting the study and specific organizations that may inspect
// or copy research data for quality assurance, such as the IU Institutional Review Board or
// its designees or the Office for Human Research Protections (OHRP).
// Digital records will be kept indefinitely as endorsed by the National Institutes of
// Health. Data, with no links to your identity, will be kept indefinitely. If for any reason you
// decide to withdraw from the study, either while in progress or after completing the
// procedure, digital records of you will be destroyed.</p>

// <p align="left">For the protection of your privacy, this research is covered by a Certificate of
// Confidentiality from the National Institutes of Health. The researchers may not disclose
// or use any information, documents, or specimens that could identify you in any civil,
// criminal, administrative, legislative, or other legal proceeding, unless you consent to it.
// Information, documents, or specimens protected by this Certificate may be disclosed to
// someone who is not connected with the research:</p>

// <p align="left">(1) If there is a federal, state, or local law that requires disclosure (such as to
// report child abuse or communicable diseases);</p>
// <p align="left">(2) if it is used for other scientific research in a way that is allowed by the federal
// regulations that protect research subjects</p>
// <p align="left">(3) for the purpose of auditing or program evaluation by the government or
// funding agency</p>

// <p align="left">You should understand that a Certificate of Confidentiality does not prevent you from
// voluntarily releasing information about yourself. If you want your research information
// released to an insurer, medical care provider, or any other person not connected with
// the research, you must provide consent to allow the researchers to release it.</p>

// <p align="left"><b>FUTURE USE</b></p>
// <p align="left">Information collected from you for this study may be used for future research studies or
// shared with other researchers for future research. If this happens, information which
// could identify you will be removed before any information are shared. Since identifying
// information will be removed, we will not ask for your additional consent.</p>

// <p align="left"><b>COMPENSATION</b></p>

// <p align="left">For participating in this study, you will receive $2.50.</p>

// <p align="left">CONTACT</p>
// <p align="left">If you have any questions about the study or the procedures, you may contact the
// researcher, <b>Chen Yu, at Indiana University, Department of Psychology, 1101 East
// 10th Street, Bloomington, IN 47405, 812-856-1920, or email chenyu@indiana.edu.</b>
// For questions about your rights as a research participant or to discuss problems,
// complaints or concerns about a research study, or to obtain information, or offer input,
// contact the IU Human Subjects Office at (812) 856-4242 or by email at irb@iu.edu</p>

// <p align="left">PARTICIPATION</p>
// Your participation in this study is voluntary. You may choose not to take part or may
// leave the study at any time. Leaving the study will not result in any penalty or loss of
// benefits to which you are entitled. Your decision whether or not to participate in this
// study will not affect your current or future relations with the investigator(s).

// <p align="left"><b>CONSENT</b></p>

// <p align="left">By checking below, you acknowledge that you have read and understand the above
// information, that you are 18 years of age or older, and give your consent to participate in
// our internet-based study.</p>

// <p align="left"><b>Thank you for agreeing to participate in our research. Before you begin, please
// note that the data you provide may be collected and used by Amazon as per its
// privacy agreement. Additionally, this research is for residents of the United
// States over the age of 18*; if you are not a resident of the United States and/or
// under the age of 18, please do not complete this survey.</b></p>

// <p align="center"><input type="checkbox" id="consentBox">
// I agree to take part in this study.
// </p>`];





var consent = {
    type: 'survey-html-form',

    on_load: function() {
        // Remove progress bar from screen
        document.getElementById("jspsych-progressbar-container").style.visibility = "hidden";
    },
    
    preamble: `
  

        <p align="left">Multimodal Learning in the Lab/online Study</p>

    <p align="middle"><b>UNIVERSITY OF TEXAS AT AUSTIN INFORMED CONSENT STATEMENT FOR RESEARCH</b></p>
    <p align="middle"><b>INFORMED CONSENT STATEMENT</b></p>
    
    <p align="left"><b>ABOUT THIS RESEARCH</b></p>
    <p align="left">You are invited to participate in a research study of language learning. We are interested
    in how people learn words and categories. We are mainly concerned with how humans
    learn to associate words with referents. We are not interested in the particular behaviors of particular individuals.
    This consent form will give you information about the study to help you decide whether you want to participate.  
    Please read this form, and ask any questions you have, before agreeing to be in the study.</p>

    <p align="left"><b>THINGS YOU SHOULD KNOW:</b></p>
    <p align="left">(1) The purpose of the study is to study language learning.</p>
    <p align="left">(2) To be eligible to consent to participate, you must be a native or fluent English speaker.</p>
    <p align="left">(3) During the study, you will be asked to pay attention to the screen as you see videos/pictures and listen to sounds/words. You may be asked questions about the stimuli during the study.</p>
    <p align="left">(4) There are no risks to participating in this study that are greater than everyday life.</p>
    <p align="left">(5) There is no direct benefit for participating in this study. You will receive a small compensation.</p>
    <p align="left">(6) Taking part in this research study is voluntary. You do not have to participate, and you can stop at any time.</p>
    <p align="left">More detailed information may be described later in this form. </p>

    <p align="left"><b>TAKING PART IN THIS STUDY IS VOLUNTARY</b></p>
    <p align="left">Your participation in this study is voluntary. You may choose not to take part or may leave the study at any time.  
    Leaving the study will not result in any penalty or loss of benefits to which you are entitled.  
    Your decision whether or not to participate in this study will not affect your current or 
    future relations with the investigator(s). </p>

    <p align="left"><b>HOW MANY PEOPLE WILL TAKE PART?</b></p>
    <p align="left">If you agree to participate, you will be one of approximately 1,500 people who will be participating 
    in this research study.</p>

    <p align="left"><b>WHAT WILL HAPPEN DURING THE STUDY?</b></p>
    <p align="left">The entire study will last 20 minutes. You will be asked to study some videos/pictures
    while listening to some sounds/words. You may be asked to learn which sound/word
    goes with which referent in the visual stimuli. During or after this experiment, your
    performance will be automatically collected. These data help us assess learning over the course of the experiment.</p>

    <p align="left"><b>WHAT ARE THE RISKS OF TAKING PART IN THE STUDY?</b></p>
    <p align="left">There is potential risk of loss of confidentiality. This risk is minimized by the investigator, 
    as outlined in the confidentiality section.</p>

    <p align="left"><b>WHAT ARE THE POTENTIAL BENEFITS OF TAKING PART IN THE STUDY?</b></p>
    <p align="left">There are no direct benefits to the subjects. However, the findings will give us more information about how people link words to object categories.</p>


    <p align="left"><b>HOW WILL MY INFORMATION BE PROTECTED?</b></p>
    <p align="left">Your identity will be held in confidence in reports in which the study may be
    published. The digital record and data will be saved on a password-protected computer
    in a locked laboratory. The data collected from you will be made available only to
    trained experimenters conducting the study and specific organizations that may inspect
    or copy research data for quality assurance, such as the IU Institutional Review Board or
    its designees or the Office for Human Research Protections (OHRP).</p>
    
    <p align="left"> Digital records will be kept indefinitely as endorsed by the National Institutes of
    Health. Data, with no links to your identity, will be kept indefinitely. If for any reason you
    decide to withdraw from the study, either while in progress or after completing the procedure, digital records of you will be destroyed.</p>

    <p align="left">For the protection of your privacy, this research is covered by a Certificate of
    Confidentiality from the National Institutes of Health. The researchers may not disclose
    or use any information, documents, or specimens that could identify you in any civil,
    criminal, administrative, legislative, or other legal proceeding, unless you consent to it.
    Information, documents, or specimens protected by this Certificate may be disclosed to someone who is not connected with the research:</p>

    <p align="left">(1) If there is a federal, state, or local law that requires disclosure 
    (such as to report child abuse or communicable diseases);</p>
    <p align="left">(2) if it is used for other scientific research in a way that is allowed by the federal regulations
    that protect research subjects</p>
    <p align="left">(3) for the purpose of auditing or program evaluation by the government or funding agency</p>

    <p align="left">You should understand that a Certificate of Confidentiality does not prevent you from
    voluntarily releasing information about yourself. If you want your research information
    released to an insurer, medical care provider, or any other person not connected with the research, 
    you must provide consent to allow the researchers to release it.</p>

    <p align="left"><b>WILL MY INFORMATION BE USED FOR RESEARCH IN THE FUTURE?</b></p>
    <p align="left">Information collected from you for this study may be used for future research studies or
    shared with other researchers for future research. If this happens, information which
    could identify you will be removed before any information are shared. Since identifying
information will be removed, we will not ask for your additional consent.</p>

    <p align="left"><b>WILL I BE PAID FOR PARTICIPATION? </b></p>
    <p align="left">For participating in this study, you will receive $2.50.</p>

    <p align="left"><b>WHO SHOULD I CALL WITH QUESTIONS OR PROBLEMS?</b></p>
    <p align="left">For questions about the study contact the researchers at the <b>Department of Psychology, 108 E. Dean Keeton Street, Austin, TX 78712, or email chenyulab@austin.utexas.edu.</b> You can contact the Principal Investigator, Chen Yu, directly at chen.yu@austin.utexas.edu.
    For questions about your rights as a research participant, to discuss problems, complaints, or concerns about a research study, or to obtain information or to offer input, please contact the UT Austin Office of Research Support and Compliance at 512-471-8871 or at <b>orsc@uts.cc.utexas.edu</b>.
    
    </p>

    <p align="left">CAN I WITHDRAW FROM THE STUDY?</p>
 <p align="left">Your participation in this study is voluntary.You may choose not to take part or may
leave the study at any time.Leaving the study will not result in any penalty or loss of
benefits to which you are entitled.Your decision whether or not to participate in this
study will not affect your current or future relations with the investigator(s).</p>

<p align = "left"><b>CONSENT TO PARTICIPATE IN RESEARCH</b></p >

    <p align="left">By checking below, you acknowledge that you have read and understand the above
    information, that you are 18 years of age or older, and give your consent to participate in
our internet-based study.</p>

    <p align="left"><b>Thank you for agreeing to participate in our research. Before you begin, please
    note that the data you provide may be collected and used by Amazon as per its
    privacy agreement. Additionally, this research is for residents of the United
    States over the age of 18*; if you are not a resident of the United States and/or
under the age of 18, please do not complete this survey.</b></p>'`,
    html: `
    <p align="center"><input type="checkbox" id="consentBox">
I agree to take part in this study.
</p>`
}