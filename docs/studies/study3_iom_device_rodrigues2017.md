## **Evaluation of a Head-Tracking Pointing Device for Users with Motor Disabilities** 

## Andreia Sias Rodrigues 

Federal University of Pelotas - PPGC (UFPel), Federal Institute South Rio-Grandense - WeTech (IFSul) P.O. Box 15.064-91.501-970 Pelotas - RS, Brasil andreia.sias@inf.ufpel.edu.br 

Vinicius Kruger da Costa Federal University of Pelotas - PPGC (UFPel), Federal Institute South Rio-Grandense - WeTech (IFSul) P.O. Box 15.064-91.501-970 Pelotas - RS, Brasil viniciusdacosta@pelotas.ifsul.edu.br 

Rafael Cunha Cardoso Federal University of Pelotas - PPGC (UFPel), Federal Institute South Rio-Grandense - WeTech (IFSul) P.O. Box 15.064-91.501-970 Pelotas - RS, Brasil rafaelcardoso@pelotas.ifsul.edu.br 

Marcio Bender Machado Federal Institute South Rio-Grandense - WeTech (IFSul) Pelotas - RS, Brasil marciomachado@pelotas.ifsul.edu.br 

Marcelo Bender Machado Federal Institute South Rio-Grandense - WeTech (IFSul) Pelotas - RS, Brasil marcelo@ifsul.edu.br 

Tatiana Aires Tavares Technology Development Center - Federal University of Pelotas (UFPel) / WeTech (IFSul) P.O. Box 15.064-91.501-970 Pelotas - RS, Brasil tatiana@inf.ufpel.edu.br 

## **ABSTRACT** 

## **KEYWORDS** 

People with disabilities generally do not have the same access to health care, education and employment opportunities. It is known that, very o￿en, they do not receive the support they need, and end up experiencing the taste of exclusion to perform their daily activities. Analyzing the overall rates of people with disabilities, it is possible to perceive that social inclusion of minorities is not a simple task. One of these daily activities is the use of information technology. Considering the cost of commercial Assistive Technology devices are very expensive for developing countries like Brazil, we proposed a comparative evaluation between the low-cost wearable head-based device and the performance values obtained in Kurauchi et al. [8] work, to analyses the viability of this low-cost device. ￿is Experimental results indicate that IOM presented a better accuracy than the two other devices, providing accurate mouse pointer positioning. Even though the speed of the low-cost IOM device was very similar than the devices analyzed and compared, the most signi￿cant result was the low-cost device accuracy was 100% , error rate was 0%. 

Low-cost IOM device, motor user disabled, Human-Computer Interaction, assistive technology, head-based mouse-replacement interface 

## **ACM Reference format:** 

Andreia Sias Rodrigues, Vinicius Kruger da Costa, Rafael Cunha Cardoso, Marcio Bender Machado, Marcelo Bender Machado, and Tatiana Aires Tavares. 2017. Evaluation of a Head-Tracking Pointing Device for Users with Motor Disabilities. In _Proceedings of PETRA 17, Island of Rhodes Greece, June 21-23, 2017,_ 7 pages. 

DOI: h￿p://dx.doi.org/10.1145/3056540.3056552 

## **1 INTRODUCTION** 

￿ere are already many projects involving di￿erent areas of knowledge developing new applications of Human-Computer Interaction (HCI) on Assistive Technology. A project in this area regards to the creation of a low cost device called IOM (Interface Oculos MOuse, in Portuguese) [10] in the South Rio-grandense Federal Institute at Pelotas (RS). 

￿is device is composed by a simple frame with two sensors, gyroscope and accelerometer, that track the head movement. Such device allows people use head and eyes movements to control the computer tasks. ￿e IOM enables an alternative interaction style to mouse and keyboard controls to upper limbs disabled users, controlling the cursor motion through the head movement and the action of mouse click [17], by se￿ing a time by dwell-time. 

## **CCS CONCEPTS** 

• **Human-centered computing** → **Pointing devices; Accessibility technologies;** _Heuristic evaluations; Pointing; Accessibility systems and tools;_ 

￿e project is currently under development but it is already patented, having tested prototypes ready for its posterior industrialization. ￿at will enable an a￿ordable lower cost device when compared to many existent devices with the similar purpose. ￿e most of devices that enable users with motor disabilities interact with computer is video-based and eye-based or eye-tracking [4, 5, 8, 18]. 

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for pro￿t or commercial advantage and that copies bear this notice and the full citation on the ￿rst page. Copyrights for third-party components of this work must be honored. For all other uses, contact the owner/author(s). _PETRA 17, Island of Rhodes Greece_ 

Although eye tracking interfaces obtained even be￿er performance than the traditional mouse (hand motion) in the speed aspect, 

> © 2017 Copyright held by the owner/author(s). 978-1-4503-5227-7/17/06...$15.00 DOI: h￿p://dx.doi.org/10.1145/3056540.3056552 

156 

PETRA 17, June 21-23, 2017, Island of Rhodes Greece 

A. Rodrigues et. al. 

however, the accuracy of current eye trackers is not su￿cient for a satisfactory pointing in real time [8]. In addition, eye-tracking devices have higher costs than video-based systems, for example, because they require more sophisticated apparatus. 

Considering the cost of commercial AT devices are very expensive for developing countries like Brazil, we proposed a comparative evaluation between the low-cost wearable head-based device IOM [10], and the performance values obtained in [8], to analyse the viability of this low-cost device. 

## **2 RELATED WORKS** 

Individuals with severe movement impairments may not be able to control a mouse or work with a conventional keyboard. If movement impairment resulted from neurological disease, such as amyotrophic lateral sclerosis (ALS), they may also not be able to use a speech recognition system, such as an input interface [14]. 

Several projects in Human-Computer Interaction (HCI) area are under development or have already been developed in order to facilitate and enable users with motor disabilities to access the computer, as shown in Table 1. 

Some examples of these devices are switches, joysticks and pointing devices activated by the body movements as show in [2]; computer screen virtual keyboard simulator so￿wares and speech recognition systems [13]; eye movement controlled by video based systems [5, 18]; devices that control head movements [12]; and more sophisticated devices employing the electric potential of the brain using EEG signals - electroencephalography, signals received by the eye movements using EOG - electrooculography [16] or contraction signals of voluntary muscles using EMG - electromyography [15] and even interfaces controlled by the brain, and brain-computer interface (BCI) together with a combination of brain sensors [6]. 

￿e detection of head movements can be done through video cameras, de￿ned as video-based or camera-based, or by a device a￿ached to the head with sensors that capture these movements, called head-based or head-track. Other motion capture method, is the face monitoring, which detects the region of the nose and mouth to control the mouse pointer. Alternatively, eye tracking (eye-based or gaze tracking) positions the mouse cursor at the estimated position of the user eyes [1]. 

Eye tracking interfaces obtained even be￿er performance than the traditional mouse (hand motion) in the speed aspect, however, the accuracy of current eye trackers is not su￿cient for a satisfactory pointing in real time [8]. It proposed a more than one movement use technique to capture the cursor movement, head movement and eye tracking, called HMAGIC (Head Movement And Gaze Input Cascaded Pointing). ￿e mouse pointer is activated by the direction of gaze and head movements the user makes for ￿ne-tuning. ￿e idea is to combine the advantages of speed of eye movements with the precision of the head movements. ￿e results a￿ested that a hybrid system proposes got be￿er accuracy. 

Other related works use the camera-mouse so￿ware [4] to capture head movements, by recognizing the face and using the user nose as a central point. In [9] was added a algorithm to the cameramouse to avoid accidental clicks, a popup window allows the user to con￿rm the click, if it is inside a period of time that you can not be sure that you really wanted click the object in focus. 

Azmi [2] proposes a ready-to-use sensor system, known as Commercial-O￿-￿e-Shelf (COTS), which features a low-cost device that enables people with motor disabilities to interact with computer. A Wii controller (Wiimote) and an infrared LED (IR) glasses were used. ￿e Wiimote was a￿ached to the glasses. ￿ese devices track the movement of the head. ￿e Windows API (Application Programming Interface) was applied to move the pointer to the correct position according to the position picked up by the Wiimote. Microso￿SAPI (Speech Application Programming Interface) made voice command recognition. ￿e browser was developed to provide a graphical user interface (GUI) for use by people with physical disabilities. ￿e total cost of the system was less than $50. In this work no evaluation of the experiment was proposed. 

Montanini [13] presents an application for people with speech and motor disabilities to type messages on a virtual keyboard on mobile devices, in real time. It provides voice synthesis and message composition based on detection of speci￿c points on the face, nose for example, and tracking by head movement. ￿e proposed application runs on portable devices with the Android Operating System. ￿e app was developed with the native libraries of this system. At this way, the available camera sensors are scanned and the computational requirements of the mobile devices are identi￿ed. ￿e prototype was evaluated and the experimental results demonstrated e￿cacy in the recognition of the user movements and the reliability of the message composition and also considered that the speech synthesis functionality were satisfactory. 

In Biswas [5] a target prediction model for cursor movement was developed which combines di￿erent multimodal input of eye movement tracking and a joystick that can reduce pointing and select task times. Its target audience is military , mainly cockpit of combat aircra￿and for computer novice users, as well as users with motor disabilities. ￿e experiments con￿rmed that users could perform signi￿cantly faster tasks using the proposed tracking system. 

Martins [12] proposes the FaceTracking algorithm for a touchless user interface, which allows anyone to control a computer without using a keyboard, mouse or touchscreen. By reusing Microso￿ Kinect sensors from videogames consoles, a cost-reduced, easy to use, and open-source interface was developed, allowing control of a computer using only the head, eyes or mouth movements, with the possibility of complementary sound commands. 

To evaluate this proposal, an inquiry was done to know the comfort level felt by users, and their feedback including improvement suggestions. Relevant user biometrics data were collected in order to facilitate further analysis, including gender, age, skin, eye color, hair, etc., including other facial accessories as well as computer literacy/experience. Eight able bodied volunteers were recruited, of which three gave up during the calibration and training phase. ￿e reasons for withdrawal were reported as: one was due to the di￿culty to control the mouse pointer (it was too sensitive to the movements performed with the head), the other complained of great discomfort when using the system, including neck pain. ￿e third one had bifocal lenses, and the fact he has to switch between the lens regions to see close/far created a great di￿culty and discomfort during system calibration. 

￿e tongue drive system proposed by HUO [7] is a wearable tongue interface that can wireless detect several user-de￿ned tongue positions inside the 3D oral space, and translate them into a set of 

157 

Evaluation of a Head-Tracking Pointing Device for Users with Motor Disabilities PETRA 17, June 21-23, 2017, Island of Rhodes Greece 

**Table 1: HCI devices as Assistive Technology and its costs for users with motor disabilities.** 

|Assistive Tech-|Assistive Tech-|Assistive Tech-|Cost of HCI Device|Based-movements|Based-movements||Tests with motor|System description|
|---|---|---|---|---|---|---|---|---|
|nology|||||||disabled users||
|Click|Control||Webcam and so￿ware|Video-based||and|Yes.<br>One student|Prevents accidental clicks (involuntary|
|[9]|||Camera Mouse. With-|gesture-based (face||and|with cerebral palsy|movements) through a screen to cancel|
||||out estimated cost|hands)||||the click. Can work with any mouse|
|||||||||controller system.|
|User|Tracking||e70 for the necessary|Video-based (Microso￿|||No.<br>Eight young,|Natural movements using kinect in|
|[12]|||hardware|Kinect sensors)|-|face|able-bodied partici-|recognition of the face, eyes, nose,|
|||||(head, nose, eyes||and|pants|mouth (open, closed) and di￿erent|
|||||mouth)||||sounds to click.|
|HMagic||[8]|Pupil Pro -e1390|Video-based (head) +|||No. Eight students,|Cascading eye movements (speed) +|
|||||eye track|||able-bodied partici-|head movements for precision.|
||||||||pants||
|Tongue||drive|O￿-the-shelf<br>com-|Movement|based||Yes.<br>On thirteen|￿is system consists of a headset that|
|[7]|||ponents,<br>including a|(tongue)|||subjects with high-|transmits (wireless) data captured by|
||||wireless<br>headphone.||||level SCI.|sensors on the user’s mouth. Managing|
||||Without estimated cost|||||to capture the rotary movements of the|
|||||||||tongue.|
|Snap||Clutch|Tobii X120 Eye Tracker|Eye-based|||Yes. Four users with|Move the eyes to pointer control in|
|[18]|||- U$34.900||||cerebral palsy and 2|games. For entertainment purpose.|
||||||||with muscular dys-||
||||||||trophy||
|Eye-Gaze [5]|||Tobii<br>TX-2<br>eye-gaze|Gaze-tracking -|oculog-||No.<br>Eight young,|A HOTAS joystick with the eye-gaze|
||||tracker<br>-<br>U$45.900|raphy|||able-bodied partici-|tracking system to be used in parallel|
||||￿rustmaster<br>Hotas||||pants|with the mouse.|
||||Warthog<br>Joystick<br>-||||||
||||U$439.95||||||
|2D|cursor-to-||Electrodes on the sur-|Capture face|signals||Yes. Six able-bodied|Two EMG sensors capture two muscles|
|target [15]|||face of the skin overly-|muscles (sEMG)|||users|of the face to be the X and Y coordinates|
||||ing a super￿cial muscle.|||||on the screen.|
||||Without estimated cost||||||
|Wiimote [2]|||Wii controller U$50 at-|Head-tracking pointer|||No|Windows API, the WiiLab and also the|
||||tached to glasses LED.|and speech||||SAPI (speech recognition) and so￿ware|
||||Without estimated cost|||||that includes the Wii and Glasses LED|
|||||||||control (IR) and captures the head move-|
|||||||||ments.|
|Camera||Mouse|Webcam and so￿ware|Video-based, face track|||Yes. With 12 users|Capture of the head movements to move|
|[4]|||Camera Mouse. With-|(head, nose, mouth||and|with disabilities|and stop at certain objects to select time|
||||out estimated cost|eyes)||||(dwell click).|
|Head|tracking||Webcam and so￿ware|Video-based (face)|||Yes|Used in mobile devices, captures the|
|and virtual key-|||Camera Mouse. With-|||||image with a camera and an overlay|
|board interface|||out estimated cost|||||keyboard image (developed), where the|
|[13]||||||||user can see more clearly where the|
|||||||||nose points.|
|IOM|-|Low-|Glasses with two sen-|Head-tracking pointer|||No. With ten stu-|It is composed by a glasses with two sen-|
|Cost||device|sors (gyroscope and ac-||||dents, able-bodied|sors (gyroscope and accelerometer) that|
|[10]|||celerometers) . About||||participants|allow people use head and eyes move-|
||||U$40 (Brazil R$150)|||||ments to control the computer tasks.|



user-de￿ned commands in real time without requiring the tongue to touch or press against anything. ￿ese commands can then be used to access a computer, operate a powered wheelchair or control other devices. 

Vickers [18] describes a middleware Snap Clutch, an approach to designing and adapting a gaze interaction technique to support locomotion to immersive game playing and also to interact with computer. ￿is was evaluated by a group of young people with 

158 

PETRA 17, June 21-23, 2017, Island of Rhodes Greece 

A. Rodrigues et. al. 

**Figure 1: IOM device overview.** 

cerebral palsy (four users) and muscular dystrophy (two users). It was developed using the Tobii SDK, but is also compatible with the Eye Tracking Universal Driver. ￿e architecture of Snap Clutch is such that new gaze-interaction techniques can be created quickly and added for use by the application. ￿e results showed that by adapting the interaction technique, participants were able to signi￿cantly improve their in-game character control. 

In PEREZ-MALDONADO [15] the proposal solution was the Surface EMG signals, it can be measured by positioning electrodes on the surface of the skin overlying a super￿cial muscle. ￿ey acquired the sEMG signals of the Auricularis Superior muscle to manipulate the position of the cursor to hit three separate ￿xed target points on the screen. ￿ey suggested that a muscle is essentially used as an electrical signal generator to drive di￿erent devices. ￿is type of user interface could be especially bene￿cial to high spinal cord injury patients and other paralyzed persons who can control head/face muscles, by providing a new option to interact with the computer and so world around them. 

An overview of these assistive technology devices and their estimates costs in HCI for motor disability users is presented at Table 1. 

## **3 THE LOW-COST IOM DEVICE (IOM - INTERFACE OCULOS MOUSE)[´]** 

￿e IOM system, represented in Figure1, is composed by a frame with two sensors (gyroscope and accelerometer) that allow people use head and eyes movements to control the computer tasks. ￿e IOM enables an alternative interaction style to mouse and keyboard controls. Hence, such solution can be very useful for upper limbs motor disabled users. 

￿is device is characterized as glasses frame that, may or not, contain the ocular lenses, according to the user needs. ￿rough the sensors embedded in the glasses, it captures positioning and head inclination. 

Besides making possible the interaction with the computer handsfree, other goals of this device IOM is to develop a low-cost, lightweight and comfortable assistive technology. At this purpose we use prototypes, presented in Figure2 in preliminary design stage to evaluate their performance according to these requirements . 

**Figure 2: Glasses Frame and hardware of Low-Cost IOM device.** 

## **4 EVALUATION PROCEDURE** 

Many tests have been applied, as a way to quantify and qualify the low-cost device IOM user experience (UX) in relation to the GUI (Graphic User Interface) control. A qualitative approach, in order to evaluate the UX and usability with oriented tasks, resulted in the quantitative data analysis for continual low-cost device IOM improvement. Although the project focuses on the development of AT for people with motor disabilities, it was decided at that time to apply the tests in able-bodied users. ￿is is done due to the fact that when we test this device directly with people with motor disabilities, it generates an expectation of immediate use of a product that is still in its initial development cycle. 

We consider that the work in which we compare the values [8] also made the evaluation process in abled bodied users. Also it was considered that the feedback from a typical user will be approximated in basic concepts of cognitive ergonomics, since the tests there is a restriction only use the low-cost IOM as HCI device without any other apparatus. 

Also it was considered that the feedback from a typical user will be approximated in basic concepts of cognitive ergonomics, since the tests there is a restriction only use the low-cost IOM as HCI device without any other apparatus. 

According to [3], the test of driving process follows the steps below, which were used in evaluation methods: Test planning, Organization of material, Local preparation, Pilot test, Choice of users, Test driving, Result analysis. ￿e target audience for the evaluation tests was composed by students of the institution and the operating system used in the test (Microso￿Windows) for activities development. 

## **4.1** _**Participants**_ 

￿e experiment was conducted with the objective of evaluating the performance metrics of the low-cost device IOM as a replacement for the traditional mouse device. A total of 10 volunteers, 4 women and 6 men between the ages of 18 and 35, able-bodied students participated in the experiment at IFSUL - Campus Pelotas between November 21th and 25th of 2016. Eight of them were students and had never used any device or so￿ware based on eye or head movements in controlling the pointer at GUI. Half of these users wear 

159 

Evaluation of a Head-Tracking Pointing Device for Users with Motor Disabilities 

PETRA 17, June 21-23, 2017, Island of Rhodes Greece 

**Figure 3: Experimental interface [11]. ￿e four possible combinations of target distances (300 and 500 pixels) and sizes (50 and 100 pixels) shown here, when grouped in a random order, de￿ne a block.** 

**Figure 4: Movement speed averaged over the trials for each experiment participant, mode, target size and distance for the three device in [8] and the low-cost IOM device.** 

glasses, either continuously or as an accessory for sun protection or reading. 

## **4.2** _**Procedure**_ 

￿e experiment involved common tasks of pointing and selecting that are used as metrics to verify the performance of a computer interface according to Fi￿s law (ISO/TS 9241-411:2012 [11] standard). ￿e activity was proposed using the low-cost device IOM in order to compare the values with the tests made in Kurauchi et al. [8]. ￿e interface is shown in Figure3. We used 13 circular targets, arranged in a circle in the center of the screen. Two distances between the circles (300 and 500 pixels, approximately 12 and 20 cm) and two measures of circle diameter (30 and 60 pixels, approximately 1.5 and 3 cm) were tested, covering four combinations, with 13 tracks in each combination. 

## **4.3** _**Dwell Time**_ 

In order to evaluate the IOM device, we used the head movements to control the pointer, and the standard click (le￿bu￿on) was performed a￿er the pointer was stopped on the target for a certain period of time, _dwell time_ . ￿e dwell time threshold was set as 750 ms. As soon as the user selected a target another one would turn red so it could be hit. If the click occurred outside the highlighted target, the error will be counted and the experiment will continue normally. 

For quantitative metric, the motion speed was computed as D / (TS - 750ms), where D is the distance between the initial and ￿nal position of a motion sequence, and the TS is time in seconds that the pointer A point that was up to the highlighted target. ￿e time of 750 milliseconds to e￿ect the click was disregarded. All the metrics were according to Kurauchi et al. [8]. 

## **4.4** _**The comparison**_ 

In Kurauchi et al. [8] they conducted an experiment to evaluate the performance of HMAGIC pointing and compare di￿erences between its use with remote and head-mounted eye trackers. 

**Figure 5: Evaluation with Low-Cost IOM device by User.** 

￿e average movement speed for the three modes presented in [8] to mouse pointer control with the 

- (1) head only (Head) 

- (2) head and remote eye tracker (RET) 

- (3) head and head-mounted eye tracker (HMET) 

￿us we compared two implementations of HMAGIC (RET and HMET) and the traditional interface based only on head movements (Head) with the Low-cost IOM device without any eye-tracker device, the graph is represented in Figure4. 

## **5 RESULTS AND DISCUSSION** 

We recorded the movement speed of low-cost IOM device, target distances, target diameter and averaged for this experiment participants over their trials, show in Figure5 . ￿e average movement speed for the three modes presented in Kurauchi et al. [8] to mouse pointer control with the (1) head only (Head), (2) head and remote eye tracker (RET), and (3) head and head-mounted eye tracker (HMET). ￿us we compared two implementations of HMAGIC (RET and HMET) and the traditional interface based only on head movements (Head) with the low-cost IOM device without any eye tracker. 

160 

PETRA 17, June 21-23, 2017, Island of Rhodes Greece 

A. Rodrigues et. al. 

**Table 2: Average movement speeds in pixels/s and standard deviations (in parenthesis) over participants for every mode, distance (300 and 500 pixels) and diameter (50 and 100 pixels) and compare with low-cost IOM device.** 

||Head|Head|RET|RET|HMET|HMET|Low-Cost IOM|Low-Cost IOM|
|---|---|---|---|---|---|---|---|---|
||**300**|**500**|**300**|**500**|**300**|**500**|**300**|**500**|
|50|231.12|322.99|407.01|599.98|364.65|548.16|442.08|509.54|
||(37.38)|(58.42)|(102.59)|(186.21)|(63.08)|(155.19)|(51.55)|(52.56)|
|100|247.11|364.71|435.67|649.85|400.09|595.01|359.58|464.03|
||(61.65)|(69.31)|(103.31)|(186.09)|(69.30)|(148.18)|(32.00)|(25.67)|



￿e mean and standard deviations of the movement speeds over all participants for every combination of mode, distance and diameter are reported in Table 2. Most notable, the average speed for low-cost IOM device and both HMAGIC implementations is higher than the average speed for the head-only mode with camera-mouse. ￿e approximate standard deviation demonstrates the stability and accuracy of the IOM device. 

Even though the speed of the low-cost IOM device was very similar than the device HMAGIC analyzed in Kurauchi et al. [8], the most signi￿cant result was the low-cost IOM device accuracy was 100% (error rate was 0% ). 

￿is metrics of Table 2 proves the e￿ciency of the low-cost IOM device evaluated. Obviously when the tests are done with the target audience, the motor disabled users, we must compare it to another tool that they have already had access to for the mouse movement, or even those that had no communication apparatus at their ￿ngertips, will be a gateway to the digital world, enabling its digital inclusion. 

## **6 CONCLUSION AND FUTURE WORK** 

￿rough the comparative Table 1 we can see that several studies show the use of the head and eyes movements as good techniques to be used as a control in HCI devices, especially considering the scenario of assistive technology focused on people with motor disabilities. Cost is clearly an important factor considering the target audience, and shown by the Table 1, the IOM device has an advantage in this regard. 

In this paper we presented the metrics of the Low-cost wearable IOM device and compared it with the head movement and gaze input cascaded (HMAGIC) method to position the mouse pointer. ￿e results shows a good performance on the pointer movement speed and accuracy compared to a video head-movement-based mousereplacement interface. ￿e low-cost IOM device also requires more practice, a learning curve for users, to get more consistent comparative results of IOM 

￿e experiment was valid so that we could evaluate the performance of the low-cost device IOM and then compare with the other devices studied that are also classi￿ed as an assistive technology, as well as the device of the case study. ￿e user experience is another extremely important factor that will need to be analyzed and veri￿ed, and whether these metrics are su￿cient for the evaluation of a pointing device for people with severe motor physical disability. 

For further work is necessary to apply new tests with speci￿c protocols and an increasing systematization of the results of the IOM compared to other assistive technologies that use the same 

principle of interaction, in order to generate a ￿nal product more enjoyable and usable by users with motor disabilities. 

## **ACKNOWLEDGMENTS** 

We would like to thank the following collaborators: 

- Kkrishna Ferreira Chavier, WeTech researcher and student at IFSul. Contact: tsixav@gmail.com 

- Jamir Alves Peroba, WeTech researcher and student at IFSul. Contact: perobajamir@gmail.com. 

We would also like to thank the volunteers who experimented with our system and the entire research group WeTech: Wearable Technology for their valuable comments and helpful suggestions. ￿e work is supported by the CNPq - Conselho Nacional de Desenvolvimento Cient´ı￿co e Tecnol´ogico h￿p://www.cnpq.br. 

## **REFERENCES** 

- [1] Amer Al-Rahayfeh and Miad Faezipour. 2013. Eye tracking and head movement detection: A state-of-art survey. _IEEE journal of translational engineering in health and medicine_ 1 (2013), 2100212–2100212. 

- [2] Aqil Azmi, Nawaf M Alsabhan, and Majed S AlDosari. 2009. ￿e Wiimote with SAPI: Creating an accessible low-cost, human computer interface for the physically disabled. _International Journal of Computer Science and Network Security_ 9, 12 (2009), 63–68. 

- [3] Albert Badre. 2002. _Shaping Web usability: interaction design in context_ . AddisonWesley Professional. 

- [4] Margrit Betke, James Gips, and Peter Fleming. 2002. ￿e camera mouse: visual tracking of body features to provide computer access for people with severe disabilities. _IEEE Transactions on neural systems and Rehabilitation Engineering_ 10, 1 (2002), 1–10. 

- [5] Pradipta Biswas and Pat Langdon. 2015. Multimodal intelligent eye-gaze tracking system. _International Journal of Human-Computer Interaction_ 31, 4 (2015), 277– 294. 

- [6] Maria Hakonen, Harri Piitulainen, and Arto Visala. 2015. Current state of digital signal processing in myoelectric interfaces and related applications. _Biomedical Signal Processing and Control_ 18 (2015), 334–359. 

- [7] Xueliang Huo. 2011. Tongue drive: a wireless tongue-operated assistive technology for people with severe disabilities. (2011). 

- [8] Andrew Kurauchi, Wenxin Feng, Carlos Morimoto, and Margrit Betke. 2015. HMAGIC: head movement and gaze input cascaded pointing. In _Proceedings of the 8th ACM International Conference on PErvasive Technologies Related to Assistive Environments_ . ACM, 47. 

- [9] Christopher Kwan, Isaac Paque￿e, John J Magee, Paul Y Lee, and Margrit Betke. 2011. Click control: improving mouse interaction for people with motor impairments. In _￿e proceedings of the 13th international ACM SIGACCESS conference on Computers and accessibility_ . ACM, 231–232. 

- [10] Marcio Machado et al. 2010. Oculos Mouse: Mouse Controlado pelos movimentos[´] da cabec¸a do usu´ario. Brazilian Patent INPI n. PI10038213. (2010). 

- [11] Sco￿MacKenzie. 2016. Fi￿sTaskTwo (2D) -Fi￿sLaw So￿ware. h￿p://www.yorku. ca/mack/Fi￿sLawSo￿ware/. (2016). 

- [12] Joao MS Martins, Jo˜ ao MF Rodrigues, and Jaime AC Martins. 2015.˜ Low-cost Natural Interface Based on Head Movements. _Procedia Computer Science_ 67 (2015), 312–321. 

- [13] Laura Montanini, Enea Cippitelli, Ennio Gambi, and Susanna Spinsante. 2015. Low complexity head tracking on portable android devices for real time message composition. _Journal on Multimodal User Interfaces_ 9, 2 (2015), 141–151. 

161 

Evaluation of a Head-Tracking Pointing Device for Users with Motor Disabilities 

PETRA 17, June 21-23, 2017, Island of Rhodes Greece 

- [14] Diogo Pedrosa and Maria da Grac¸a C. Pimentel. 2014. Text Entry Using a Foot for Severely Motor-impaired Individuals. In _Proceedings of the 29th Annual ACM Symposium on Applied Computing (SAC ’14)_ . ACM, New York, NY, USA, 957–963. DOI:h￿p://dx.doi.org/10.1145/2554850.2554948 

- [15] Claudia Perez-Maldonado, Anthony S Wexler, and Sanjay S Joshi. 2010. Twodimensional cursor-to-target control from single muscle site sEMG signals. _IEEE Transactions on Neural Systems and Rehabilitation Engineering_ 18, 2 (2010), 203– 209. 

- [16] Carlos G Pinheiro, Eduardo LM Naves, Pierre Pino, Etienne Losson, Adriano O Andrade, and Guy Bourhis. 2011. Alternative communication systems for people with severe motor disabilities: a survey. _Biomedical engineering online_ 10, 1 (2011), 1. 

- [17] Andreia Sias Rodrigues, Vinicius da Costa, M´ arcio Bender Machado, Ang´ elica Lac-´ erda Rocha, Joana Marini de Oliveira, Marcelo Bender Machado, Rafael Cunha Cardoso, Cleber ￿adros, and Tatiana Aires Tavares. 2016. Evaluation of the Use of Eye and Head Movements for Mouse-like Functions by Using IOM Device. In _International Conference on Universal Access in Human-Computer Interaction_ . Springer, 81–91. 

- [18] Stephen Vickers, Howell Istance, and Aulikki Hyrskykari. 2013. Performing locomotion tasks in immersive computer games with an adapted eye-tracking interface. _ACM Transactions on Accessible Computing (TACCESS)_ 5, 1 (2013), 2. 

162 

