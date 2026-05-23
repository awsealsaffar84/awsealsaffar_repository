# **Designing and Evaluating Head-based Pointing on Smartphones for People with Motor Impairments** 

Muratcan Cicek 

University of California, Santa Cruz Santa Cruz, CA mcicek@ucsc.edu 

## Ankit Dave 

## Wenxin Feng Michael Xuelin Huang Julia Katherine Haines Jefrey Nichols 

{ankitdave,wenxinfeng,mxhuang,juliahaines}@google.com jef@jefreynichols.com Google LLC Mountain View, CA 

## **ABSTRACT** 

Head-based pointing is an alternative input method for people with motor impairments to access computing devices. This paper proposes a calibration-free head-tracking input mechanism for mobile devices that makes use of the front-facing camera that is standard on most devices. To evaluate our design, we performed two Fitts’ Law studies. First, a comparison study of our method with an existing head-based pointing solution, Eva Facial Mouse, with subjects without motor impairments. Second, we conducted what we believe is the frst Fitts’ Law study using a mobile head tracker with subjects with motor impairments. We extend prior studies with a greater range of index of difculties (IDs) [1.62, 5.20] bits and achieved promising throughput (average 0.61 bps with motor impairments and 0.90 bps without). We found that users’ throughput was 0.95 bps on average in our most difcult task (IDs: 5.20 bits), which involved selecting a target half the size of the Android recommendation for a touch target after moving nearly the full height of the screen. This suggests the system is capable of fne precision tasks. We summarize our observations and the lessons from our user studies into a set of design guidelines for head-based pointing systems. 

## **CCS CONCEPTS** 

• **Human-centered computing** → **User studies** ; Empirical studies in accessibility; **User centered design** ; • **Social and professional topics** → _People with disabilities_ . 

## **KEYWORDS** 

Mobile Devices, Accessibility, Input Techniques, Head-based Iointing, User-Centered Design 

Work has been completed during the frst author’s internship at Google LLC. 

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for proft or commercial advantage and that copies bear this notice and the full citation on the frst page. Copyrights for third-party components of this work must be honored. This work is licensed under a Creative Commons Attribution International 4.0 License. For all other uses, contact the owner/author(s). _ASSETS ’20, October 26–28, 2020, Virtual Event, Greece_ 

© 2020 Copyright held by the owner/author(s). ACM ISBN 978-1-4503-7103-2/20/10. https://doi.org/10.1145/3373625.3416994 

## **ACM Reference Format:** 

Muratcan Cicek, Ankit Dave, Wenxin Feng, Michael Xuelin Huang, Julia Katherine Haines, and Jefrey Nichols. 2020. Designing and Evaluating Head-based Pointing on Smartphones for People with Motor Impairments. In _The 22nd International ACM SIGACCESS Conference on Computers and Accessibility (ASSETS ’20), October 26–28, 2020, Virtual Event, Greece._ ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3373625.3416994 

**Figure 1: A user is using our mobile head tracker.** 

## **1 INTRODUCTION** 

Head-based pointing (HBP) is an efective input method for Virtual Reality and Gaming [6, 10, 18, 24], as well as for accessibility [4, 28, 29, 31, 34, 47]. As computer vision techniques advance, visionbased HBP has become feasible for interaction on mobile devices using their built-in hardware. HBP on smartphones can leverage the front-facing camera, and thus can be especially useful for users with hand motor impairments, since it is portable, easy to install, and requires no specialized equipment. Despite its great potential as an assistive technology, most existing HBP research has focused on desktop/stationary settings. Few studies have included participants with motor impairments [47, 51], fewer have investigated HBP on mobile devices [2, 33], and none we are aware of have explored both. To fll this research gap, we conducted the frst HBP Fitts’ Law study on smartphones with users with motor impairments and quantitatively studied its practicality with throughput (Fitts’ index of performance [15]). Through these standardized outputs, one may compare any pointing methodology with our results and claim its practicality for people with motor impairments. 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

Cicek et al. 

Based on the lead author’s lifelong experience using HBP, we identify three major requirements for the design of our mobile head tracker. It should 1) be easy to use and require no cumbersome settings or calibration before or during use; 2) support precise pointing to match the requirements expected by typical user interface designs; and 3) be confgurable and adaptive to personal needs. This paper then proposes a low-cost, device-independent, calibrationfree pointing technique based on head tracking using the frontfacing camera on mobile devices. It uses the neural-network-based face detection to provide pixel-level precision and allows for multiple selection methods, including dwell time, smile, and blink. To further ensure its customizability and truly enable personalization at scale, we will open source our Android implementation upon acceptance. 

The user studies of our mobile HBP not only show its efectiveness compared with the state-of-the-art Eva Facial Mouse (EFM) [33], but also shed light on future directions for mobile HBP for assistive technology in general. The design of our studies followed previous practice [46] of Fitts’ Law studies on mobile devices. We conducted two user studies to evaluate Fitts’ Law performance across users with and without motor impairments (see Figure 1). The frst one is a between-subjects user study with 42 participants without motor impairments, to compare our technique with an existing product (Eva Facial Mouse) and provide a baseline to understand the performance diference across user groups. The second study was performed with 15 participants with motor impairments. It revealed a number of invaluable lessons and edge cases. Three participants in the second study participated remotely in uncontrolled environments, demonstrating the robustness of our method to various device settings and lighting conditions. The experimental results show that our mobile HBP can work across environments and devices, for users with diferent degrees of motor impairments, and the throughput of our technique compares favorably with previous work [13, 28, 33] under similar conditions. Therefore, we recommend HBP for users with motor impairments as an alternative interaction method on mobile devices. 

Our contributions are three-fold: 

- (1) We designed and refned a calibration-free mobile headbased pointing mechanism based on the in-depth lessons learnt from motor impairment experience; 

- (2) We conducted the frst Fitts’ Law study on participants with motor impairments on small-screen mobile devices, performed a comprehensive evaluation and analyzed with quantitative results, compared the proposed method with the state of the art [33] and suggest a set of guidelines for future accessibility studies of mobile HBP; 

- (3) We open-sourced the proposed HBP[1] framework to allow for personalized mobile HBP at scale. 

## **2 RELATED WORK** 

While we propose an alternative approach for smartphone interaction that may be generally useful for all, our work primarily focuses on users with motor impairments with a goal to improve their access to mobile devices. Pointing and scrolling are two key tasks that are required to interact successfully with mobile devices. 

> 1Implementation at https://github.com/muratcancicek/mobile_head_based_pointing 

The pointing abilities of those with motor impairments have been frequently investigated, as described in the next sub-section, and alternative methods have been proposed to ease pointing tasks for those with motor impairments. Head-based techniques have also been evaluated as a pointing method. 

## **2.1 Pointing Ability of People with Motor Impairments** 

Fitts [15] designed and ran the frst experimental study evaluating human performance in target acquisition tasks. His seminal work became known as Fitts’ Law and has adapted countless times to many related input tasks. The ISO 9241 standard [21] includes variations of his work for testing the performance of non-keyboard input devices. Fitts’ Law techniques have also been used to evaluate pointing performance tasks for specifc user groups, including individuals with motor impairments. One of the frst Fitts’ Law studies in this latter category was conducted by Bravo et al. [7] to compare the reaction and movement times between able-bodied and cerebral palsied groups and concluded that the cerebral palsied group required more time to respond. Riviere and Thakor [43] also showed that movement disorders make mouse use quite inaccurate and nonlinear. Montague et al. [36] found similar performance and interaction behaviors for motor-impaired users using touchscreens on mobile devices. Similarly, Findlater et al. [14] compared touchscreen and mouse input performance by people with and without upper body motor impairments. These studies and Wobbrock [48] show that pointing at targets in graphical user interfaces, whether with a mouse, a stylus, or a touch screen, is still a serious access barrier for people with motor impairments because of the required fne-motor skills. This has led researchers to work on improving the efciency of pointing tasks through alternate methods. 

## **2.2 Alternative Pointing Methods** 

The head-mounted stylus is one of the oldest alternative pointing devices, in which a stylus is mounted on the end of a long stick that is afxed to the user’s head via a hat or headband. Users move their hand to tap location on a screen, or it can be used as a writing tool by attaching a regular pencil to the end of the stylus. Physical headmounted styluses are still in use today [41] for touchscreens, and new sophisticated products like Quha Zono [40] and Glassouse [17] provide hardware that one may attach to their body and transmit head movements to a computer via Bluethooth. 

Many alternative pointing technologies have been developed, including several adaptive mouse solutions [37], screen scanning mechanisms [20], gaze-based mechanisms [20, 23, 30, 35, 38, 49], and head-based solutions [11, 25, 32, 33, 39]. Adaptive mouse requires a special large-size touchpad, and as such is not as amenable to mobile use. Screen scanning has a low throughput via twodimensional scanning, but is the only solution for certain types of severe impairments like advanced ALS. In contrast, both gazeand head- based pointing techniques ofer reasonable throughput and can make use of the built-in camera already present on most mobile phones provided the user has good control of their head or eyes. Comparisons between head-based and gaze-based interactions [3, 24] suggest that head-based techniques are more voluntary, stable and have greater accuracy while gaze-based techniques may 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

Designing and Evaluating Head-based Pointing on Smartphones for People with Motor Impairments 

be faster for some specifc tasks like typing [16]. Work is ongoing to increase gaze accuracy on mobile platforms [19, 22, 42], but as of today practical mobile gaze-based interactions are still challenging. 

Some of today’s alternative pointing methods employ visualbased interactions [31] that detect and track the voluntary movement of a body part [47] for two-dimensional pointing. Betke et al. [4] show that visual tracking of body features, especially facial (e.g. face, nose, eyebrow), can be a successful pointing tool for people with motor impairments. Mauri et al. [34] also review assistive technologies and conclude that visual-based systems could be the only means of computer interaction for some users. Advantages to the visual approach include fexibility and lower cost over other traditional assistive technologies. Head-based pointing is an example of a visual-based approach, and today there are several successful applications of head-based pointing for assistive technology (e.g. Camera Mouse [39], Smyle Mouse [25], Enable Viacam [32], HeadMouse Nano [11], EVA Facial Mouse [33]). Head-based tracking has also been applied in other areas, including desktop GUIs [5], wearable computing [8], and VR 3D user interface [6, 10, 24]. 

## **2.3 Evaluation of Head-Based Pointing on Mobile** 

Today, there are several mobile head-tracking solutions available on Android phones, such as EVA Facial Mouse (EFM) [33] and Essential Accessibility [2]. Both provide control of the mobile environment without requiring an external device, nor requiring sensitive calibration. Unfortunately, we are not aware of any previous studies evaluating these solutions. This absence led us to include the evaluation of EFM in this study as a competitor to our own proposed method. On the other hand, recent studies have evaluated head-tracking on mobile devices [1, 45–47] using iOS and tablet platforms instead of phones. In their frst study, Roig-Maimó et al. [47] propose two similar tasks to evaluate head-tracking, a picture-revealing puzzle game for pointing and an item selection task for diferent sized items. A later evaluation explored a diferent pointing task design [45]. In their most recent work, Roig-Maimó et al. [46] apply a Fitts’ law performance evaluation to a mobile head-tracking interface by following the multi-directional tapping test described in the ISO standard [21]. To the best of our knowledge, these are the frst and still only Fitts’ law studies on user performance of head-tracking interfaces with mobile devices. Our study goes beyond the previous work by including individuals with motor impairments as participants. 

## **3 DESIGNING A MOBILE HEAD-BASED POINTING SYSTEM** 

This section describes the design principle for our mobile HBP. The lead author’s more than 10 years of personal experience using similar technologies provided inspiration for the following list of design requirements. 

## **3.1 Motivation** 

The lead author of this paper, a person with motor impairments, has an immediate need for a head-tracking mechanism that provides pointing functionality on mobile. While the author has benefted from HBP in stationary desktop settings for years, the number 

of available solutions on mobile is limited. With a few exceptions, existing mobile HBP solutions either lack an objective evaluation [2, 33] or are not publicly available [2, 44, 47] for further development. One recent study [9] both properly evaluated and open-sourced its implementation, however its head-tracking relied on specialized hardware. Here, we develop an HBP technique that can function on a wider range of devices that feature a front facing camera, such as the vast majority of smartphones. 

## **3.2 Personal User Experience** 

Despite living with signifcant motor impairments, the lead author has pursued a career requiring heavy computer usage. This has led to the over ten years of experience with head-based pointing on a number of computing devices, and thus insight into the essential design requirements for an HBP method. All of the lead author’s work on this paper, including the implementation of the method, designing the pointing tasks, and writing the academic paper were done through the use of HBP methods. Ultimately, this work presents an interaction method for people with motor impairments that is designed and developed by a person with motor impairments. 

## **3.3 Base Requirements for Mobile Head-based Pointing** 

Based on personal experiences with head-based pointing, we summarize a list of requirements that we consider critical for HBP on mobile devices with small screens: 

- Hardware-free: our mobile HBP should exploit existing builtin sensors and be standalone. Requiring additional nonstandard assistive hardware would undermine its availability and usability. As such, we employ a completely vision-based method that relies on the standard front-facing cameras available on today’s smartphones. 

- Customizable: we understand that users’ physical abilities vary across individuals. A usable HBP should be able to adapt to basic personal needs. Therefore, our HBP is designed to provide set of selection options, including dwell, blink, and smile, to provide a degree of customizability to the user’s ability level. 

- Calibration-free: calibration is generally intrusive to user experience, and perhaps even tedious and time-consuming if frequent re-calibration is required. To improve in-situ usability and mitigate the dependency on the external supervision from a person without motor impairments, our HBP is designed to be calibration-free. 

- Precise: on-screen visual targets can be very close, particularly on mobile devices, sometimes making target selection challenging even for people without motor impairments. To address this, our HBP must be able to provide precise pointing while requiring minimal physical efort by the user. 

- Available and extendable: besides making the mobile device accessible, the solution itself also should be available and extendable by third parties for other potential users. To meet these two requirements, we believe the solution must be open-sourced. 

These requirements help us to refne the existing technology on mobile and carefully choose the implementation tools to build on. 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

**==> picture [33 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
Cicek et al.<br>**----- End of picture text -----**<br>


To avoid biasing by our personal experience alone, we conducted multi-person evaluations of our HBP mechanism, which will be discussed in a later section. 

## **4 IMPLEMENTING MOBILE HEAD-BASED POINTING** 

According to the above requirements, we developed an HBP algorithm for mobile devices. Our system frst detects the head and key facial information from the front-facing camera on a smartphone. It then utilizes the coordinate of the nose tip and maps its movement onto the on-screen cursor location. 

## **4.1 Platform and Libraries** 

We implemented our HBP algorithm on Android so it can be available for a large population of potential users in both the developed and developing world. We used the Flutter (futter.dev) UI toolkit for the user interface and ML Kit for Firebase to track facial features using the front-facing camera on mobile devices. ML Kit for Firebase is a mobile SDK with a set of ready-to-use machine learning APIs. Its face detection API allows us to detect faces in an image, identify key facial features, and retrieve the detected face contours. It also provides high-level facial information such as eye openness and smiling, which we use to implement the selection methods. 

Given these of-the-shelf toolkits, our technical challenge becomes two-fold: 

- (1) To map the movement of the identifed facial features into the movement of an on-screen pointer; and 

- (2) To implement selection methods that translate facial gestures or lack of head movement into a click on the screen. 

## **4.2 Mapping Head Movement to On-Screen Cursor Location** 

This section describes our mapping function from the physical head movement to the on-screen pixel coordinate. There are two types of descriptors: one is with respect to the screen coordinate, such as the pixel location of eye corners; the other is with respect to the camera coordinate, such as the estimated head pose given by the vision tracking algorithm. Our HBP opts for the former, as it is unafected by head pose estimation error and the camera intrinsic parameters across devices. 

_4.2.1 Mapping onto Cursor Relative Change v.s. Absolute Location._ As we aim to achieve calibration-free HBP, we map the head movement onto the relative change of cursor location, rather than the absolute location. This is because, in our experience, the one-to-one mapping from head location onto cursor absolute location is hard to use. In order to point at a certain on-screen location, the user has to make a specifc head pose w.r.t. the camera. This inevitably requires head calibration in practice. In case of pose change from either the user or the device, a re-calibration is needed. Such design violates our base design requirements. Instead, our mapping function incrementally changes the cursor location according to head movements. In this case, the ways to point the cursor to an exact location is non-deterministic, meaning that users have the fexibility to start from an arbitrary head pose, move their heads in a natural fashion, and gradually approach the intentional target. 

**Figure 2: A demonstration of clipping the cursor at the screen edge when head movements overshoot. This mechanism allows for the intuitive adjustment of the head-tocursor mapping.** 

_4.2.2 Clipping to the Edge of the Screen._ To truly allow for calibrationfree, our HBP introduces a clipping mechanism. That is, it clips the cursor location when the cursor reaches the screen edge and the user continues moving in the same direction. Figure 2 shows an example in which, through some occurrence, the cursor is located at the center of the screen when the user’s nose is pointed 15[◦] of center. At this point (a) the user may likely feel the need to realign the face angle with the cursor location (e.g. 0[◦] head yaw onto screen center). To accomplish this, the user can turn left (- 15[◦] ) until the cursor touches the screen edge, and (c) keep turning along the original movement (-30[◦] ). Once the cursor reaches the left edge, our HBP will discard the leftward control signal from head movements. We refer to this phase as overshoot. When the user (d) starts to move back toward the screen (0[◦] ), the cursor will start to follow from its position on the screen edge. By enabling this head movement overshoot, we believe users will be able to easily adjust the head-to-cursor mapping on the fy. We later found this to be true in our user studies. 

_4.2.3 Pointing by Nose._ A key choice in our algorithm is how to convert the extracted facial features into a two-dimensional space to guide the on-screen pointer. The main challenge is detection reliability in practice; as more components are involved, the more intrusive detection noise becomes. To alleviate this issue, we exploit just one facial feature: nose tip. Specifcally, we defne an input velocity function _Vinput_ by the nose tip pixel coordinates _nt_ on the captured image in the frame _t_ as follows: 

**==> picture [195 x 11] intentionally omitted <==**

The smoothing function on the input _Sinput_ is defned as the mean flter with an constant window length _sinput_ where 

**==> picture [183 x 29] intentionally omitted <==**

Designing and Evaluating Head-based Pointing on Smartphones for People with Motor Impairments 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

Empirically, we found that _sinput_ = 3 gives a good consistency between head and cursor when the system runs at around 40 fps. The input velocity _vinput_ = _Vinput_ ( _nt_ ) presents the input change as the user changes head position. A mapping function _ϕ_ translates _vinput_ to the output velocity _voutput_ as _voutput_ = _ϕ_ ( _vinput_ ) where 

**==> picture [206 x 21] intentionally omitted <==**

_Rimaдe_ is the resolution of the input image in units of physical pixels while _Rscreen_ is the resolution of the mobile screen in units of logical pixels. A gain factor, empirically set to _дainFactor_ = (6, 8), transforms the head motion to the cursor motion linearly and it yields consistent user perception across diferent device sizes. The output velocity _voutput_ in this formulation can be too sensitive to input changes since the scaling factors also amplifes the high-frequency noise while it reduces the physical head movement. Therefore, we introduce a motion threshold function Λ( _voutput_ ). It ignores the subtle noise and return values only greater than the predefned thresholds, i.e. Λ( _vx_ , _vy_ ) = ( _λ_ ( _vx_ , _mx_ ), _λ_ ( _vy_ , _my_ )) where 

**==> picture [171 x 28] intentionally omitted <==**

We observed that _mx_ = 5 and _my_ = 5 resulted in a good tradeof between the physical eforts to start driving the cursor and to maintain the head pose to keep the cursor stationary. We apply thresholds on each axis independently to allow the user to travel linearly along one axis while excluding the noise from the other axis. Applying Λ gives us an intermediate on-screen cursor location as _ct_ ′ where _ct_ ′ = _ct_ −1 − Λ( _voutput_ ), where _ct_ − _t_ denotes the cursor location in the last frame. 

In our design, as is common in other approaches, the cursor is required to stay within the screen when the user input would otherwise push the cursor beyond the edge. We confne the pointing space within the screen, by encapsulating the proposed location with a boundary check function _β_ as _β_ ( _ct_ ′). This function is used to achieve the re-center procedure described above. In addition to smoothing the input, the fnal pointing coordinates _ct_ also include additional smoothing on _β_ ( _ct_ ′) to improve stability and it is defned as 

**==> picture [157 x 11] intentionally omitted <==**

where _Soutput_ has the same behavior with _Sinput_ in the equation 2 and applies a mean flter with the same window length as _so_ = 3. In conclusion, the end-to-end head to cursor mapping function Φ that calculates the fnal pointing coordinates _ct_ from the given nose tip coordinates _nt_ is defned as: 

**==> picture [237 x 24] intentionally omitted <==**

Notice that Φ is designed to be device-independent by introducing scaling into logical pixels and tends to be calibration-free by only relying on relative input change. However, it also includes a set of constants { _sinput_ , _дainFactor_ , ( _mx_ , _my_ ), _soutput_ } which are predefned based on our initial exploration and kept fxed through the study. This, on the other hand, ofers the fexibility for those want to customize the mapping function Φ. It is straightforward to 

**Figure 3: Illustration of the Multi-Directional Task. Amplitude = 125 dp, Target Width = 60, Index of Difculty = 1.65 bits, corresponding to Test 1 in our experiment design. (a) The target appears on a blank screen with current test info above. The pointer is an orange crosshair. (b) In dwell selection mode, hovering over the target turns it gray and the crosshair flls indicating time until selection. (c) The next target appears immediately after selection. (d) Shows all targets for one block of a test, requiring 24 consecutive pointing tasks across 4 subspaces. The movements from the last target in one subspace to the frst target in the next are not recorded.** 

fne-tuning these parameters in an optional calibration according to the personal needs. 

_4.2.4 Selection Methods._ To provide a full mechanism that completes point-and-select tasks, we introduce multiple selection methods alongside our HBP implementation. Dwell-based selection is preferable when the available input channels are limited since dwelling depends on users’ behavior with the pointing mechanism as a selection is fred when the pointer is kept within a constrained region (dwelling circle) for a certain time period. We found that a dwelling diameter of _d_ = 20 logical pixels and a dwelling time of _p_ = 0.8 seconds work well with our algorithm. We also implemented smiling and blinking as visual selection methods and also included them in our user study. 

## **5 EVALUATION METHOD** 

To evaluate the pointing performance of our implementation objectively, we employ a Fitts’ Law [15] pointing task since it is the standard way to evaluate pointing methods and derive the dependent measure of throughput (Fitts’ index of performance) as part of the comparison and evaluation [45]. This section describes the common elements of our evaluation across our two experiments. Details where the procedure or apparatus varied will be discussed in the next section. 

## **5.1 Multi-directional Corner Task** 

The standard multi-directional pointing task (MD) described in the ISO 9241-9 standard [21] employs a circular arrangement of targets that does not fully utilize the long rectangular shape of most mobile devices screens. Using this arrangement is possible, but the range of possible indices of difculty would not be representative of real world mobile device tasks because the longer dimension of the 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

Cicek et al. 

device is not explored. Roig-Maimó et al. [46] noted this challenge and developed a new Multi-Directional Corner task which takes better advantage of the space available on a mobile screen while maintaining some consistency with the standard task. We replicate this method in our studies, though with a wider range of indices of difculty. 

The Multi-directional Corner Task [46] consists of four "subspaces," each of which starts with a target in one corner of the device screen, then requires the user to choose one of three targets on an arc a fxed radius from the initial target, and then return to select the initial target. This results in six pointing tasks per subspace. After completing one subspace, the user must select the initial target for the next subspace and then targets within that subspace using the same approach. This gives a total of 24 pointing tasks per "block." Note that only targets selected within a subspace are used for evaluation, and movements between targets in diferent subspaces were not included in our analysis. Please refer to the Figure 3. 

For most trials, users completed three blocks at each difculty level. We reduced the number of blocks in some conditions to address fatigue or time constraints, as discussed later in the paper. 

The vast majority of trials with our software, and all of the trials with Eva Facial Mouse, made use of the dwelling selection method to select targets. Some trials conducted with our software made use of our blinking and smiling selection techniques, but often just to get users’ impressions of the techniques rather than conduct a formal evaluation. 

## **Table 1: Fitts’ Law Performance of Comparison Participants** 

||||**A**|**W**|**ID**|**MT**|**MT**|**TP**|**TP**|
|---|---|---|---|---|---|---|---|---|---|
||**Test**|**SM**|**(dp)**|**(dp)**|**(bit)**|**(s)**|**(stdev)**|**(bps)**|**(stdev)**|
|**EFM**|**1**|D|125|60|1.62|**2.96**|0.22|**0.62**|0.10|
||**2**|D|535|60|3.31|**3.57**|0.52|0.88|0.13|
||**3**|D|125|30|2.37|3.05|0.20|**0.76**|0.08|
||**4**|D|535|30|4.24|**3.69**|0.35|**1.06**|0.13|
|||||**Grand**|**Mean**|**3.32**|0.28|0.83|0.09|
|**HBP**|**1**|D|125|60|1.62|**1.89**|0.30|**0.84**|0.12|
||**2**|D|535|60|3.31|**3.06***|0.37|0.88*|0.11|
||**3**|D|125|15|3.22|3.02|0.40|**0.92**|0.13|
||**4**|D|535|15|5.20|**4.57**|0.68|**0.95**|0.15|
|||||**Grand**|**Mean**|**3.14**|0.34|0.90|0.10|
||**5**|B|535|60|3.31|3.43*|0.80|0.80*|0.20|
||**6**|S|535|60|3.31|3.09*|0.58|0.83|0.14|



**Study includes two experiment designs as EFM and HBP. These designs include three Selection Methods (SM) include Dwelling (D), Blinking (B) and Smiling (S). In the cells, the asterisks (*) indicate that diference between those values and the corresponding values in Test 2 were statistically signifcant (p < 0.05) within the HBP design. Also, the corresponding Bold values in two designs indicate their diferences to each other were statistically signifcant (p < 0.05). The p values were calculated based on two-tailed t-tests with type 1 and type 2 respectively in these comparisons.** 

## **5.2 Apparatus and Procedure** 

All of our experiments were conducted on Android devices, with the vast majority of subjects using a Google Pixel 2 device with a 5-inch display with 1920x1080 resolution (441 ppi). The phone was placed on a mount, which was stuck to the table immediately in front of the subject’s chair at a distance of two feet. The only variation from this was for the small number of remote participants with motor impairments, who each used their personal Android device and placed it as was comfortable for their environment. We implemented a custom Head Pointing Test App, which implemented the Multi-directional Corner Task [46] mentioned above and was installed on the devices in advance of the experiment. The entire testing procedure took place within the app. 

Participants were recruited through the recruitment service of a large technology company. Every participant signed a consent form before beginning the study, and also provided responses to a pre-study questionnaire which collected details such as previous experiences with related technology, whether they wear glasses, and basic demographic information. Afterward, participants were briefed about the goal of the study, were shown the running software, and allowed to play with a practice mode of the testing application for as long as they desired. Most users practiced for less than one minute. During the practice, we instructed participants on the self-calibration technique and asked them to fnd a comfortable position so that they could point at all corners of the screen. We also informed them that they were free to take breaks or stop at any point. 

Once they were ready to begin, we started the frst block of the study. After each block, the user had the opportunity to rest, and then either the subject or the experimenter could press an on-screen button to start the next block. In the able-bodied experiments, subjects generally continued to the next block on their own, whereas the experimenter often helped the subjects in the motor impairment experiments. 

Following the study, participants were asked to fll out a post study questionnaire, which allowed participants to comment on the interaction methods and any fatigue they may have been feeling. For most experiments, participants needed 30 minutes to complete the study. 

## **5.3 Throughput Calculation** 

For each sequence of trials that the subject completed consecutive pointing tasks, we calculated throughput (TP) as follows: 

**==> picture [195 x 20] intentionally omitted <==**

where _MT_ is averaged movement time per trial and _IDe_ is derived as: 

**==> picture [159 x 21] intentionally omitted <==**

where _Ae_ is the mean of the actual movement amplitudes and _We_ is the efective target width, calculated as _We_ = 4.133 · _SDx_ , where _SDx_ is the standard deviation in the selection coordinates as well-defned by MacKenzie [26]. The units of TP are "bits per second (bps)" since _IDe_ and _MT_ have units of "bits" and "seconds" respectively. 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

Designing and Evaluating Head-based Pointing on Smartphones for People with Motor Impairments 

Note that we used the standard-deviation method to calculate throughput [27] following the same strategy as Cuaresma and MacKenzie [12]. This is because our specifc design utilizes dwelling function and has no _error rate_ [50]. One may fnd the details of the throughput calculation in the previous work [12, 26, 46, 50]. 

## **6 EXPERIMENTS** 

We conducted two evaluation experiments of our head-based pointing system. 

- (1) **Comparison with the state-of-the-art.** We compared our algorithm against Eva Facial Mouse [33], a freely available head-based pointing method for Android to show statistically how the state-of-the-art HBP performs on mobile and how comparable our performance is against this. Able-bodied participants were recruited for this comprehensive Fitts’ Law study where numerous participants complete various pointing tasks as we inferred this study could not be so practical with participants with motor impairments. 

- (2) **Exploration with participants with motor impairments.** We evaluated our algorithm with participants with motor impairments in several settings. We generally used the same procedure for these experiments as for the comparison study, though it was necessary to make modifcations to suit the abilities of some participants. In this study, our goal was not so much to understand the Fitts’ Law performance characteristics but to understand users’ varied experiences. 

## **6.1 Comparison with Eva Facial Mouse** 

Our frst evaluation compared our technique to Eva Facial Mouse (EFM) [33], which. is a refned piece of commercial software with a lot of bells and whistles (e.g., a drag and drop mode, long tap, etc.) that is freely available for Android. In this experiment, we used a between-subjects design with each participant experiencing just one of the two pointing methods. The main reason for this choice was time, as it is much easier at our institution to recruit for a 30minute study than a 60 minute study, and we found 30 minutes to be the minimum time needed to evaluate a single technique. Learning efects and fatigue were other concerns. Participants reported minor issues with fatigue in our study, such as dry eyes, but none dropped out. We suspect fatigue would have become a greater concern and some participants would have dropped out with a 60-minute study, which would have complicated our analysis. 

_6.1.1 Participants._ Forty-two able-bodied participants (16 females) were recruited from the employees of a large technology company using that company’s user study recruitment service. The ages of participants ranged from 18 to 52 with a mean of 31.79 years (SD = 7.14). It was a prerequisite of participation that participants did not identify as a person with motor impairments and were not sufering from any injuries that might impact their ability to use a head-based pointer (e.g., a neck injury). Participants were compensated the equivalent of $15 US in internal corporate credits. 

_6.1.2 Procedure._ All studies were conducted in interior conference rooms of the large technology company. Target widths and distances are listed in 1 for all trials. 

20 participants used our pointing method and 22 used Eva Facial Mouse. In both cases, participants were told that they were testing pre-release software and not informed of the actual provenance of the software until after completing the post-study questionnaire. 

Besides the pointing software, there were two additional diferences between the study conditions. Due to a mistake in software confguration, the smaller target width difered: 30dp in the Eva Facial Mouse condition and 15dp in the condition with our software. The discrepancy was noticed too late to correct it without throwing away the work of nearly all participants in one of the conditions. Throughput calculations take into account diferences in target width, so we believe the results can still be taken up with confdence. Participants using our software completed two extra tests, one each using the blinking and smiling selection methods in order to collect feedback on these other options. These tests consisted of one block of tasks at a single index of difculty. While we calculate throughput for these tasks for completeness, these values should be considered with caution. All other tests in both conditions used the dwelling selection method. 

_6.1.3 Results._ We report the Fitts’ Law performance of participants in Table 1 for each test in addition to a grand mean of participants which was calculated from participants’ individual performances. The grand means for movement time and throughput were 3.20 s and 0.87 bps respectively for our method. The standard deviation of throughput at 0.05 across all dwelling trials indicates our method performs consistently across diferent Index of Difculties without requiring calibration. 

In the comparison of the two methods, we observe that the movement times and throughput values for the participants who used our method were strongly correlated to the test’s Index of Difculty (ID) while the participants who used Eva Facial Mouse seem to demonstrate non-linear performance as difculty increases. Figure 4 shows that two methods reach the same efciency around ID of 4 while HBP outperforms at lower IDs which values are actually more common in mobile environments. We ran a two-tailed t-test with type 2 (between-subjects) to evaluate whether there was a diference between the conditions. In Tests 1 & 4, the easiest and hardest tests in both experiment designs, we measured that the performance diferences between HBP and EFM were statistically signifcant (p < 0.05) in terms of the moment times and throughput values. However, the diference in throughput values in Test 2 and the diference in movement times in Test 3 were not statistically signifcant. There was no signifcant diference between overall throughput but there was a signifcant diference in overall movement time (p < 0.05). The insignifcance in the other tests and overall throughput could be the result of close performances around the intermediate IDs, as HBP and EFM seem to behave similarly around ID = 4 bits while HBP may be superior at the edge cases. 

Tests 2, 5 and 6 (Table 1) in HBP design, all at the same index of difculty, can be compared to get a sense of the diferences between selection methods. Performance seems remarkably similar across these tasks, though they performed slightly better with dwelling and achieved a throughput of 0.88 bps while they only achieved 0.80 bps with blinking and 0.83 bps with smiling. The diferences between dwelling and other two methods respectively were statistically signifcant (p < 0.05 in both cases) although the performance 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

Cicek et al. 

diference between blinking and smiling methods was not statistically signifcant. The p values were calculated based on two-tailed t-tests with type 1. More trials would need to be conducted with the alternate selection methods to reach a conclusive result. 

**Table 2: Fitts’ Law Performance of Participants with Motor Impairments Within-Test and Within-Experiment Design** 

||||||**A**|**W**|**ID**|**MT**|**TP**|
|---|---|---|---|---|---|---|---|---|---|
||**Test**|**SM**|**P**|**Bs**|**(dp)**|**(dp)**|**(bit)**|**(s)**|**(bps)**|
|**FP1**|**1**|D|4|3|250|60|2.37|5.34|0.44|
||**2**|D|1|3|250|40|2.86|2.81|0.94|
|**FP2**|**1**|D|5|2|550|40|3.88|7.92|0.78|
||**2**|B|2|2|550|40|3.88|3.16|0.95|
||**3**|D|2|2|550|20|4.88|3.81|1.09|
|**R**|**1**|D|3|3|125|60|1.62|2.38|0.80|
||**2**|D|3|3|535|60|3.31|2.91|1.15|
||**3**|B|3|1|535|60|3.31|4.53|0.78|
||**4**|D|3|3|125|30|2.37|2.45|0.95|
||**5**|D|3|3|535|30|4.24|3.81|1.00|
||**6**|S|3|1|535|60|3.31|2.26|1.11|



**Study includes three experiment designs as Field Phase 1 (FP1), Field Phase 2 (FP2) and Remote (R). These designs include three Selection Methods (SM) include Dwelling (D), Blinking (B) and Smiling (S). Participation (P) and number of blocks (Bs) in each test also vary.** 

## **6.2 Exploration with participants with motor impairments** 

After conducting our comparison study, we were interested to see how our method might fare with our target user population. We found that reaching such participants was challenging, and thus we carried out two sub-experiments with two diferent subpopulations: 

A feld study at Ability Now Bay Area, a non-governmental organization that ofers adults with developmental and physical disabilities a variety of programs, including education, wellness and community integration. 

A remote study with participants with motor impairments recruited by the user study recruitment service of the same company in the comparison study. These participants installed our software on their own phones and participated in a video conference while they completed the pointing tasks. 

_6.2.1 Participants._ Sixteen participants (8 females) were recruited in total from two diferent sources. Ages ranged from 25 to 65 with a mean of 38.2 years (SD = 16.05). There were no requirements on prior experience to participate in the study except identifying as a person with motor impairments. Field study participants were compensated the equivalent of $100 US in gift cards; remote participants were compensated the equivalent of $75 also in gift cards. The diference in compensation is due to the shorter anticipated duration of the remote study. 

We recruited 13 feld study participants. Due to their severe physical limitations, 5 participants were not able to complete any tasks, while 8 participants completed at least one of the given tasks. In all cases, the participants were able to provide valuable feedback on the usefulness of the technique. 

The three remote participants were much more capable on average than the feld study participants. Each had a diferent type of motor impairment. Each was able to install the software on their own device and complete all trials. 

_6.2.2 Procedure._ The procedure generally followed that for the comparison study, though we had to make modifcations for the setting and participants’ ability levels. 

The remote participants’ experience was the closest to the comparison study. The order of trials, blocks, and the indices of difculty can be found in Table 2. The other diference with these trials is that we could not ensure consistent placement of the device compared to the comparison and feld study experiments. Participants were told not to hold the device and asked to place it on a solid surface at which it was comfortable to view the full screen. 

We originally planned for a much more comprehensive set of trials during the feld study, but found that our plan was too ambitious given the ability level of most of the feld study participants. To address this challenge, we modifed our plan in two phases: 

- _Phase 1:_ We found that participants could only complete a few tasks and we were uncertain of the validity for a Fitts’ Law study. We revised our goal to simply have participants complete trials at one, and at most two, difculty levels. 

- _Phase 2:_ After some experience with the frst phase design, we revised our design to have fewer iterations of the same task and more task variety. 

Table 2 shows the details of each design, such as the block counts for each test and Fitts’ Law parameters. As its _Participants_ column states, participation in the tests was not equal since some participants had to quit the experiment after completing just a few blocks. Two participants in phase one and three participants in phase two quit the experiment without completing any blocks. 

We were particularly careful during the feld study to ensure that participants were aware that they could rest or quit at any time. We monitored participants for frustration and fatigue, checked in on them as necessary, and reminded them of their options if we felt it was warranted. 

_6.2.3 Results._ Based on overall ability, we split the 16 participants with motor impairments into 3 subgroups. 

- (1) _The group with mild motor impairments_ includes 6 participants who have fne head control ability and were able to complete the given tasks in similar amounts of time. They reported that their physical impairments limit or completely block their interaction with smartphones via standard methods but did not afect their head-based interaction. 

- (2) _The group with moderate motor impairments_ includes 5 participants that were able to complete at least one block of the given tasks. But, the completion times were inconsistent among the participants and we observed that their overall pointing performance was low compared to the frst group. 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

Designing and Evaluating Head-based Pointing on Smartphones for People with Motor Impairments 

- (3) _The group with severe motor impairments_ includes the remaining 5 participants who were unable to complete any block of the given tasks due to the ability-related reasons while they spent approximately the same amount of time in the sessions with the other participants. 

We choose to report the means based on participants’ overall performances calculated across the tests they individually completed. We believe this is still informative given that a participant’s overall performance suggests how head-based pointing likely works for that individual. Table 3 shows that the grand mean for throughput was 0.61 bps, however we noticed that the participants with mild impairments performed noticeably better than the group with moderate impairments, and thus report the mean for each group separately as 0.96 bps and 0.20 bps. 

**Table 3: Fitts’ Law Performance of Participants with Motor Impairments.** 

|||**MT** **(s)**|**MT** **(stdev)**|**TP** **(bps)**|**TP** **(stdev)**|
|---|---|---|---|---|---|
|**Physical**|**Mild**|3.29|0.73|0.96|0.19|
|**Impairment**|**Moderate**|12.86|8.28|0.20|0.09|
|**Group**|**Severe**|N/A|N/A|N/A|N/A|
|**Experiment**|**Field** **Phase** **1**|6.30|3.33|0.53|0.31|
|**Design**|**Field** **Phase** **2**|6.47|5.17|0.87|0.27|
||**Remote**|3.19|0.89|0.97|0.21|
|**Grand** **Mean**||7.70|7.22|0.61|0.42|



Participation in the tests that explored the blinking and smiling selection methods was low (Table 2) and only included the participants in the group with mild impairments. Analyzing the results of Test 2, 3 and 6 in Design for Remote study would be a fair comparison for the selection methods as they introduced the same Index of Difculty and were performed by the same 3 participants. The participants appeared to perform slightly better with smiling than as they completed the trails slightly faster, 2.26 s and 2.91 s respectively. Blinking appears to be the slowest method with an average movement time of 4.53 s. However, the diferences were not statistically signifcant. 

## **7 DISCUSSION** 

We designed and evaluated head-based pointing (HBP) on smartphones for people with motor impairments. For the evaluation, we conducted two separate user experiments that includes participants with and without motor impairments, the frst one also includes a comparison with Eva Facial Mouse (EFM). 

## **7.1 Evaluation Against the State of the Art** 

In the comparison experiment with participants without motor impairments, the grand means for movement time and throughput were 3.14 s and 0.90 bps respectively for the proposed HBP while they were 3.32 s and 0.83 bps For EFM (Table 1). These values and indicate Figure 4 that the proposed HBP approach slightly outperforms EFM at the IDs lower than 4 bit (target widths > 30 dp). Considering Android’s Material Design principles that recommend touch target width should be at least 48 dp, HBP has superiority in the most common point tasks on mobile. For reference, HBP 

also outperforms FittsFace [12], another head-based pointing implementation and reports movement time of 7.14 s and throughput of 0.47 bps. However, our measurements stayed short compared to the original Multi-Directional Corner Task Experiment [46] where the grand means for movement time and throughput per trial were 1.41 s and 1.54 bps respectively. But, they utilized screen touch as selection method which was not practical for our target group as their fne hand control was so limited. 

_7.1.1 Takeaways._ HBP’s superiority over EFM is likely due to EFM’s earlier development and our early focus on evaluating pointing performance. We recommend our algorithm as the point to build from for future researchers and developers of HBP techniques, however we recommend EFM to everyday users with an immediate need as it is a much more polished product than our current software. 

## **7.2 Evaluation with Target User Group** 

In our second experiment with participants with motor impairments, the grand mean for throughput was 0.61 bps (Table 3), though the results also show that the performance of participants with diferent levels of impairments can vary substantially. In this case, we suggest to narrow the target user group when developing real applications with HBP and provide diferent functionalities for users from diferent ability groups. For example, one may provide multiple selection methods as optional to diferent groups. We also believe that developers also tend to build their applications for the worst case scenarios and target the group with severe impairments. However, this trend leaves out the intermediate groups out of the market. This group is not willing to be limited with very basic tools since they have greater abilities, but on the other hand they cannot fully utilize the of-the-shelf products due to their impairments. While this is just an observation and needs further investigation, this work showed that the intermediate user groups can complete complex pointing tasks at higher IDs through head-based pointing. 

_7.2.1 Limitations._ During evaluation with the target group, we noted several limitations of our study design that afected the overall results. We would like to share these limitations here as an observation and to guide the future studies with similar settings. 

Accessing and working with people with motor impairments had several limitations, including the physical ones like distance and time. In the feld, we had to recruit all the candidates with motor impairments we could access based on self reports of capabilities such as head control. However, these reports were not well calibrated and as a result our group had a much wider range of physical abilities and more signifcant impairments than we expected. Although we tried to adjust our test design accordingly, 5 participants with severe impairments could not complete the tests even though they were able to use the system. Despite the difculty, a few of these participants enjoyed using the system so much that they wanted and were allowed to continue using the system long after their scheduled time, even though they were only able to complete only a couple of the easiest trials. It seemed that these participants likely could have completed many tasks via HBP if we could have further reduced the index of difculty or had additional technology to flter spasmotic movements while the participants were trying to dwell. 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

Cicek et al. 

But, in that case, the difculty level would not be realistic for the participants with mild and moderate impairments. 

We further observed that some participants with motor impairments had conditions that made head-based pointing difcult, such as lack of stability in their chairs. While most of the participants had fne control of their heads, their conditions would cause involuntary movements of their limbs, which afected their head position and this dramatically afected their pointing performance in the Fitts’ Law Study. This was especially true during the dwelling time where they were trying to stay still. Indeed, for some participants, it seemed that trying to stay still would make involuntary spasms more likely. Interestingly, one of the highest performing participants was nearly completely restrained in his chair with his arms strapped tightly to his body, and this seemed to greatly assist him maintaining stability. Many other participants did not have this beneft, possibly because many seemed to be in loaner chairs because their main chair was being repaired. 

_7.2.2 Takeaways._ In future work, the recruitment criteria for participants with motor impairments should be narrowed down to sub-groups based on ability levels and separate test designs should be adapted for each impairment group. This helps to show the true beneft of HBP when appropriate pointing tasks are given to each group. Additionally, the potential external constraints of head-based pointing needs to be well-considered. While were we able to gather statistical results from this Fitts’ Law study, they do not necessarily show the efectiveness of HBP for the target group who has such limited options. HBP also needs to be evaluated as a communication tool for the same group by diferent measurements rather than Fitts’ Law. 

It was also interesting that few of the participants used mobile phones and most were very dependent on visiting the rehabilitation facility to be able to use a computer, which enabled them to communicate with friends and even conduct business. If we could make it possible for them to use a mobile device, then that could lead to a very big change in their independence and communication ability. Many were unaware that a free head-based pointing system (i.e. EFM [33]) was available for every day usage, except one participant who used a sophisticated head-based pointing system on a daily basis. We believe head-based pointing techniques would help many more users if they were made aware of their availability. 

To further explore head-based pointing on mobile and improve its practicality for people with motor impairments, we are considering several possibilities for future work. First, it seems that more advanced HBP techniques are needed that will work for the difcult cases and address issues such as the involuntary movements we mentioned above. Filtering out such movements might be possible using machine learning that detects spasms, based either on visual input or pointer behavior. Another possibility might be to employ an interaction technique that does not require the on-screen pointer to be tightly connected with head position at all times. For example, a "clutched" method that would somehow allow participants to disconnect the pointer from their head when a spasm occurs might be very helpful. Second, the small size of many targets on mobile user interfaces makes them difcult to use. If a system was able to understand the constructions of these user interfaces, then it might be possible to modify the user interface itself to be more usable, 

**Figure 4: Comparison of Average Trail Durations (Target-toTarget Movement Time) for HBP (n=20) and EFM (n=22) at diferent Indices of Difculty.** 

such as with larger buttons, fewer targets, etc. Such techniques would be benefcial not only for users with motor impairments, but also those with cognitive impairments and likely other conditions. 

## **7.3 Meeting the Base Requirements** 

In the section 3.3, we stated four base requirements for a robust head-based pointing solution. Here, we discuss how our proposed HBP meets these requirements. It is a _hardware-free_ solution as it does not require any external hardware and employs a completely vision-based method that relies on the standard front-facing cameras available on today’s smartphones. It is _customizable_ with diferent selection methods and performs consistently. Our frst experiment supports this as the participants achieved throughput of 0.88 bps with dwelling, 0.80 with blinking, and 0.83 with smiling at the same ID (3.31 bits). It is _calibration-free_ and performs consistently across diferent Index of Difculties and diferent user groups without requiring an initial calibration per condition. We found the performance of HBP stayed stable while Index of Difculties (IDs) increasing within the range we tested. Movement time per trial linearly increased as shown in the fgure 4 while the standard deviation of throughput at 0.05 across all IDs. We furthermore observed this behavior with HBP in both experiments with participants with and without impairment (see Tables 1 and 2). It stays _precise_ even beyond the limits of Android’s Material Design principles, which recommend that touch target width should be at least 48 dp. Our HBP method achieved throughput of 0.95 bps (above the grand mean) in an extreme setting with ID of 5.20 bits where target width was 15 dp. It will become _available_ and _extendable_ as we are considering to open source upon the publication. 

## **8 CONCLUSION** 

This paper presents a calibration-free head-tracking input mechanism for mobile devices which is easy to use, requires no additional equipment, and allows for pixel-level pointing precision on small-size screens. To verify this design, we performed two user experiments based on Fitts’ Law and this experiments include people with and without motor impairments along with another existing method for a fair comparison. It is the frst Fitts’ Law study using a mobile head tracker with participants with motor impairments and 

Designing and Evaluating Head-based Pointing on Smartphones for People with Motor Impairments 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

shows its practicality for this group by numbers. 

## **ACKNOWLEDGMENTS** 

We thank Ability Now Bay Area (Oakland, CA) for their collaboration in our feld study as they allowed us to recruit their visitors and host us for two days through the study. We thank Mai Lou Lor (Family Matters In-Home Care, LLC) for her assistance in our user studies as well as caregiving to the frst author. We also thank Cesar Mauri Loba (Universitat Rovira i Virgili) who built and opensourced Eva Facial Mouse [33] that provides head-based pointing for millions of Android users for years. 

## **REFERENCES** 

- [1] Mahdieh Abbaszadegan, Sohrab Yaghoubi, and I Scott MacKenzie. 2018. TrackMaze: A Comparison of Head-Tracking, Eye-Tracking, and Tilt as Input Methods for Mobile Games. In _International Conference on Human-Computer Interaction_ . Springer, 393–405. 

- [2] Essential Accessibility. 2018. Essential Accessibility. Retrieved August 6, 2018 from https://www.essentialaccessibility.com/assistive-technology-for-android/. 

- [3] Richard Bates and Howell O Istance. 2003. Why are eye mice unpopular? A detailed comparison of head and eye controlled assistive technology pointing devices. _Universal Access in the Information Society_ 2, 3 (2003), 280–290. https: //doi.org/10.1007/s10209-003-0053-y 

- [4] Margrit Betke, James Gips, and Peter Fleming. 2002. The camera mouse: Visual tracking of body features to provide computer access for people with severe disabilities. _IEEE Transactions on neural systems and Rehabilitation Engineering_ 10, 1 (2002), 1–10. https://doi.org/10.1109/TNSRE.2002.1021581 

- [5] Martin Bichsel and Alex Pentland. 1993. Automatic interpretation of human head movements. 

- [6] Doug Bowman, Ernst Kruijf, Joseph J LaViola Jr, and Ivan P Poupyrev. 2004. _3D User interfaces: theory and practice_ . Addison Wesley. https://doi.org/10.1162/ pres.2005.14.1.117 

- [7] Pedro E Bravo, Miriam LeGare, Albert M Cook, and Susan Hussey. 1993. A study of the application of Fitts’ law to selected cerebral palsied adults. _Perceptual and motor skills_ 77, 3_suppl (1993), 1107–1117. https://doi.org/10.2466/pms.1993.77. 3f.1107 

- [8] Stephen Brewster, Joanna Lumsden, Marek Bell, Malcolm Hall, and Stuart Tasker. 2003. Multimodal ’eyes-free’ interaction techniques for wearable devices. In _Proceedings of the SIGCHI conference on Human factors in computing systems_ . ACM, 473–480. https://doi.org/10.1145/642693.642694 

- [9] Muratcan Cicek, Jinrong Xie, Qiaosong Wang, and Robinson Piramuthu. 2018. Mobile Head Tracking for eCommerce and Beyond. _arXiv preprint arXiv:1812.07143_ (2018). 

- [10] Rory MS Cliford, Nikita Mae B Tuanquin, and Robert W Lindeman. 2017. Jedi ForceExtension: Telekinesis as a Virtual Reality interaction metaphor. In _3D User Interfaces (3DUI), 2017 IEEE Symposium on_ . IEEE, 239–240. https://doi.org/10. 1109/3DUI.2017.7893360 

- [11] Origin Instruments Corporation. 2017. HeadMouse Nano. Retrieved July 17, 2018 from http://www.orin.com/access/headmouse/. 

- [12] Justin Cuaresma and I Scott MacKenzie. 2017. FittsFace: Exploring navigation and selection methods for facial tracking. In _International Conference on Universal Access in Human-Computer Interaction_ . Springer, 403–416. https://doi.org/10. 1007/978-3-319-58703-5_30 

- [13] Gamhewage C De Silva, Michael J Lyons, Shinjiro Kawato, and Nobuji Tetsutani. 2003. Human factors evaluation of a vision-based facial gesture interface. In _2003 Conference on Computer Vision and Pattern Recognition Workshop_ , Vol. 5. IEEE, 52–52. 

- [14] Leah Findlater, Karyn Mofatt, Jon E Froehlich, Meethu Malu, and Joan Zhang. 2017. Comparing touchscreen and mouse input performance by people with and without upper body motor impairments. In _Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems_ . ACM, 6056–6061. https: //doi.org/10.1145/3025453.3025603 

- [15] Paul M Fitts. 1954. The information capacity of the human motor system in controlling the amplitude of movement. _Journal of experimental psychology_ 47, 6 (1954), 381. https://doi.org/10.1037/h0055392 

- [16] Yulia Gizatdinova, Oleg Špakov, and Veikko Surakka. 2012. Comparison of videobased pointing and selection techniques for hands-free text entry. In _Proceedings of the international working conference on advanced visual interfaces_ . ACM, 132– 139. https://doi.org/10.1145/2254556.2254582 

- [17] Glassouse. 2018. Glassouse Assistive Device. Retrieved July 17, 2018 from http://glassouse.com/. 

- [18] John Paulin Hansen, Vijay Rajanna, I Scott MacKenzie, and Per Bækgaard. 2018. A Fitts’ law study of click and dwell interaction by gaze, head and mouse with a head-mounted display. In _Proceedings of the Workshop on Communication by Gaze Interaction_ . ACM, 7. 

- [19] Qiong Huang, Ashok Veeraraghavan, and Ashutosh Sabharwal. 2015. TabletGaze: unconstrained appearance-based gaze estimation in mobile tablets. _arXiv preprint arXiv:1508.01244_ (2015). https://doi.org/10.1007/s00138-017-0852-4 

- [20] Apple Inc. 2018. Use Switch Control to navigate your iPhone, iPad, or iPod touch. Retrieved July 15, 2018 from https://support.apple.com/en-us/ht201370. 

- [21] ISO ISO. [n.d.]. 9241-9 Ergonomic requirements for ofce work with visual display terminals (VDTs)-Part 9: Requirements for non-keyboard input devices (FDIS-Final Draft International Standard), 2000. _International Organization for Standardization_ ([n. d.]). 

- [22] Kyle Krafka, Aditya Khosla, Petr Kellnhofer, Harini Kannan, Suchendra Bhandarkar, Wojciech Matusik, and Antonio Torralba. 2016. Eye tracking for everyone. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ . 2176–2184. https://doi.org/10.1109/CVPR.2016.239 

- [23] Andrew Kurauchi, Wenxin Feng, Ajjen Joshi, Carlos Morimoto, and Margrit Betke. 2016. EyeSwipe: Dwell-free text entry using gaze paths. In _Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems_ . ACM, 1952–1956. https://doi.org/10.1145/2858036.2858335 

- [24] Mikko Kytö, Barrett Ens, Thammathip Piumsomboon, Gun A Lee, and Mark Billinghurst. 2018. Pinpointing: Precise Head-and Eye-Based Target Selection for Augmented Reality. In _Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems_ . ACM, 81. https://doi.org/10.1145/3173574.3173655 

- [25] Perceptive Devices LLC. 2016. SmyleMouse. Retrieved July 15, 2018 from https://smylemouse.com/. 

- [26] I Scott MacKenzie. 2015. Fitts’ throughput and the remarkable case of touchbased target selection. In _International Conference on Human-Computer Interaction_ . Springer, 238–249. 

- [27] I Scott MacKenzie. 2018. Fitts’ Law. _The Wiley Handbook of Human Computer Interaction_ 1 (2018), 347–370. https://doi.org/10.1002/9781118976005.ch17 

- [28] John Magee, Torsten Felzer, and I Scott MacKenzie. 2015. Camera Mouse+ ClickerAID: Dwell vs. single-muscle click actuation in mouse-replacement interfaces. In _International Conference on Universal Access in Human-Computer Interaction_ . Springer, 74–84. 

- [29] John J Magee, Samuel Epstein, Eric S Missimer, Christopher Kwan, and Margrit Betke. 2011. Adaptive mouse-replacement interface control functions for users with disabilities. In _International Conference on Universal Access in HumanComputer Interaction_ . Springer, 332–341. 

- [30] Päivi Majaranta. 2011. _Gaze Interaction and Applications of Eye Tracking: Advances in Assistive Technologies: Advances in Assistive Technologies_ . IGI Global. https: //doi.org/10.4018/978-1-61350-098-9 

- [31] Cristina Manresa-Yee, Pere Ponsa, Javier Varona, and Francisco J Perales. 2010. User experience to improve the usability of a vision-based interface. _Interacting with Computers_ 22, 6 (2010), 594–605. https://doi.org/10.1016/j.intcom.2010.06.004 

- [32] Cesar Mauri. 2017. Enable Viacam. Retrieved July 15, 2018 from http://eviacam. crea-si.com/index.php. 

- [33] Cesar Mauri. 2018. EVA Facial Mouse. Retrieved July 16, 2018 from https: //github.com/cmauri/eva_facial_mouse#user-content-eva-facial-mouse. 

- [34] César Mauri, Toni Granollers i Saltiveri, Jesús Lorés Vidal, and Mabel García. 2006. Computer vision interaction for people with severe movement restrictions. _Human Technology: An Interdisciplinary Journal on Humans in ICT Environments, vol. 2, núm. 1, p. 38-54_ (2006). https://doi.org/10.17011/ht/urn.2006158 

- [35] Microsoft. 2018. Eye Control for Windows 10. Retrieved July 16, 2018 from https: //www.microsoft.com/en-us/garage/wall-of-fame/eye-control-windows-10/. 

- [36] Kyle Montague, Hugo Nicolau, and Vicki L Hanson. 2014. Motor-impaired touchscreen interactions in the wild. In _Proceedings of the 16th international ACM SIGACCESS conference on Computers & accessibility_ . ACM, 123–130. https: //doi.org/10.1145/2661334.2661362 

- [37] Martez E Mott, Radu-Daniel Vatavu, Shaun K Kane, and Jacob O Wobbrock. 2016. Smart touch: Improving touch accuracy for people with motor impairments with template matching. In _Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems_ . ACM, 1934–1946. https://doi.org/10.1145/2858036.2858390 

- [38] MyGaze. 2018. MyGaze Assistive. Retrieved July 16, 2018 from http://www. mygaze.com/products/mygaze-assistive/. 

- [39] Trustees of Boston College. 2018. CameraMouse. Retrieved July 15, 2018 from http://www.cameramouse.org/. 

- [40] Quha oy. 2018. Quha Zono. Retrieved July 15, 2018 from http://www.quha.com/ products-2/zono/. 

- [41] Ondrej Polacek, Thomas Grill, and Manfred Tscheligi. 2013. NoseTapping: what else can you do with your nose?. In _Proceedings of the 12th International Conference on Mobile and Ubiquitous Multimedia_ . ACM, 32. https://doi.org/10.1145/2541831. 2541867 

- [42] Rajeev Ranjan, Shalini De Mello, and Jan Kautz. 2018. Light-weight Head Pose Invariant Gaze Tracking. _arXiv preprint arXiv:1804.08572_ (2018). 

- [43] Cameron N Riviere and Nitish V Thakor. 1996. Efects of age and disability on tracking tasks with a computer mouse: Accuracy and linearity. (1996). PMID: 

ASSETS ’20, October 26–28, 2020, Virtual Event, Greece 

Cicek et al. 

8868412. 

- [44] Maria Roig-Maimó, Cristina Manresa-Yee, and Javier Varona. 2016. A robust camera-based interface for mobile entertainment. _Sensors_ 16, 2 (2016), 254. 

- [45] Maria Francesca Roig-Maimó, I Scott MacKenzie, Cristina Manresa-Yee, and Javier Varona. 2017. Evaluating ftts’ law performance with a non-ISO task. In _Proceedings of the XVIII International Conference on Human Computer Interaction_ . ACM, 5. https://doi.org/10.1145/3123818.3123827 

- [46] Maria Francesca Roig-Maimó, I Scott MacKenzie, Cristina Manresa-Yee, and Javier Varona. 2018. Head-tracking interfaces on mobile devices: Evaluation using Fitts’ law and a new multi-directional corner task for small displays. _International Journal of Human-Computer Studies_ 112 (2018), 1–15. https://doi.org/10.1016/j. ijhcs.2017.12.003 

- [47] Maria Francesca Roig-Maimó, Cristina Manresa-Yee, Javier Varona, and I Scott MacKenzie. 2016. Evaluation of a mobile head-tracker interface for accessibility. In _International Conference on Computers Helping People with Special Needs_ . Springer, 449–456. https://doi.org/10.1007/978-3-319-41267-2_63 

- [48] Jacob O Wobbrock. 2014. Improving pointing in graphical user interfaces for people with motor impairments through ability-based design. In _Assistive Technologies and Computer Access for Motor Disabilities_ . IGI Global, 206–253. https://doi.org/10.4018/978-1-4666-4438-0.ch008 

- [49] Xiaoyi Zhang, Harish Kulkarni, and Meredith Ringel Morris. 2017. SmartphoneBased Gaze Gesture Communication for People with Motor Disabilities. In _Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems_ . ACM, 2878–2889. https://doi.org/10.1145/3025453.3025790 

- [50] Xuan Zhang and I Scott MacKenzie. 2007. Evaluating eye tracking with ISO 9241-part 9. In _International Conference on Human-Computer Intrction_ . Springer, 779–788. https://doi.org/10.1007/978-3-540-73110-8_85 

- [51] Rafael Zuniga and John Magee. 2017. Camera Mouse: Dwell vs. Computer VisionBased Intentional Click Activation. In _International Conference on Universal Access in Human-Computer Interaction_ . Springer, 455–464. https://doi.org/10.1007/9783-319-58703-5_34 

