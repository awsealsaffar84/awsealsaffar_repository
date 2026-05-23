The Thirty-Eighth AAAI Conference on Artificial Intelligence (AAAI-24) 

# **Gaze-Based Interaction Adaptation for People with Involuntary Head Movements (Student Abstract)** 

## **Cindy Tong**[1, 3] **, Rosanna Chan**[2][*][, 3] 

1 Nanyang Technological University, Singapore 

> 2 Centre for Perceptual and Interactive Intelligence, Hong Kong 

3The Chinese University of Hong Kong, Hong Kong to0001di@e.ntu.edu.sg, yychan@ie.cuhk.edu.hk 

## **Abstract** 

Gaze estimation is an important research area in computer vision and machine learning. Eye-tracking and gaze-based interactions have made assistive technology (AT) more accessible to people with physical limitations. However, a nonnegligible proportion of existing AT users, including those having dyskinetic cerebral palsy (CP) or severe intellectual disabilities (ID), have difficulties in using eye trackers due to their involuntary body movements. In this paper, we propose an adaptation method pertaining to head movement prediction and fixation smoothing to stabilize our target users’ gaze points on the screen and improve their user experience (UX) in gaze-based interaction. Our empirical experimentation shows that our method significantly shortens the users’ selection time and increases their selection accuracy. 

## **Introduction** 

Gaze-based interaction technologies such as eye trackers are becoming more popular in our daily lives. In addition to being an access device for games and entertainment, eye trackers are also used by people with physical disabilities to access computers and communication technologies. For example, a human-computer interaction (HCI) user study shows that 90% of the participating children having mild to moderate CP could successfully interact with an experimental system using eye-tracking devices (Cruceat and Butean 2019). An extensive investigation was also performed with young children having dyskinetic CP, which is a complex form of CP (Monbaliu et al. 2017). Although all five participants completed the trial successfully, a parent expressed that the frequent necessary device re-calibration was frustrating (Karlsson, Bech, and Stone 2019). 

Most existing eye trackers are based on real-time video analyses (Vedaldi and et al. 2020), where a camera is used to detect the pupil centre and corneal reflection to estimate the user’s fixation points. This approach assumes the stability of the user’s head, which is often not the case for people having Athetoid or dyskinetic CP and some of the post-stroke 

> *This study was partially supported by the Centre for Perceptual and Interactive Intelligence (CPII) Ltd under the Innovation and Technology Commission (ITC)’s InnoHK. Copyright © 2024, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 

patients (Siniscalchi et al. 2012). These users often have involuntary abnormal movements with patterns different from natural head movements. Therefore, gaze-based interaction still remains challenging for this population group. 

In this paper, we propose and develop a new eye-tracking algorithm with involuntary head movement adaptation. Our algorithm (1) adjusts the gaze point on the screen according to the detected head position and pose, and (2) proactively controls the gaze moving speed on the screen. We have performed a preliminary user study with two participants having involuntary head movement. Our results show that the gaze-based interaction performance in both participants was effectively promoted by our adaptation approach. 

## **The Current Work** 

## **Problem Description** 

The current work investigates how computer vision and machine learning techniques can be applied to improve the gaze-based interaction experience for users having involuntary head movements. Specifically, there are two subproblems that need to be solved: 

(1) How can we maintain a smooth and accurate interaction experience even when the user’s head is not in the optimal position for the eye-tracker? 

(2) How can we stabilise the gaze trace on the user interface so as to facilitate other gaze-based interactions? 

## **Our Approach** 

Here, we propose the **head movement detection and smoothing algorithm (HMDSA)** as a solution to the above problem. HMDSA contains two key functions, namely, the head pose monitor, and the gaze points speed controller. 

**Head Pose Monitor pose** ( **g** _,_ **h** _, θ_ ) The purpose of this function is to overcome any gaze point instability due to the user’s involuntary head movement. This is particularly important for gaze-based UX, especially when the selection target is small or located at the screen corners. It produces an adapted gaze point **g** _[′]_ based on the 2-dimensional detected gaze point **g** , the 3-dimensional detected head position **h** and the y-axis Euler rotation angle of the user’s head _θ_ . 

**Gaze speed Controller speed** ( **g** _,_ **¯g** _,_ **h** _,_ **h[¯]** _, S, T, λ_ ) The purpose of this function is to oppose any sudden changes in 

23669 

The Thirty-Eighth AAAI Conference on Artificial Intelligence (AAAI-24) 

Algorithm 1: HMDSA 

**Input** : Eye-tracker detected gaze point **g** = ( _gx, gy_ ), head positionmoving-average **h** = ( _h_ gaze _x, hy, h_ point _z_ ), Euler **g** ¯ = (¯rotation _gx,_ ¯ _gy_ ), anglemoving-average(y-axis) _θ_ , head position **h[¯]** = ( _h_[¯] _x, h_[¯] _y, h_[¯] _z_ ). 

**Parameter** : Window timeframe _T_ , speed threshold _S_ , impact factor _λ_ . **Output** : Adjusted gaze point ˜ **g** = (˜ _gx,_ ˜ _gy_ ) 

- 1: Initialise **g** = **¯g** = (0 _,_ 0), **h** = **h[¯]** = (0 _,_ 0 _,_ 0), and _θ_ = 0 

- 2: **while** user interaction continue **do** 

- 3: check if gaze point is detected 

- 4: **if** no gaze point detected **then** 

- 5: **g** ˜ = **g** ¯ 6: **else** 

- 7: obtain **g** _,_ ¯ **g** _,_ **h** _,_ **h**[¯] _, θ_ adapt gaze point based on head pose: **g** _[′]_ = pose( **g** _,_ **h** _, θ_ ) adapt head position based on gaze speed: **h** _[′]_ = speed( **g** _[′] ,_ **¯g** _,_ **h** _,_ **h[¯]** _, S, T, λ_ ) compute **˜g** based on **g** _[′]_ and **h** _[′]_ 

- 8: **end if** 

- 9: update ¯ **g** _,_ **h**[¯] and output ˜ **g** 

- 10: **end while** 

head position caused by involuntary head movements. Having specified the window timeframe _T_ , the gaze speed _s_ can be derived from the current gaze point **g** and it’s moving average **¯g** by 

**==> picture [154 x 11] intentionally omitted <==**

With the speed threshold _S_ that limits the gaze speed and the impact factor _λ_ that decides the confidence level of the current measurement, our smoothing function outputs a 3- dimensional vector **h** _[′]_ as the adapted head position where: 

**==> picture [180 x 28] intentionally omitted <==**

## **User Experiment** 

## **Participants, Procedures, and Measurements** 

We have performed a within-subject HCI experiment to evaluate the effectiveness of our approach (Purchase 2012). Our participants were two patients (1 f, 1m) having involuntary head movements caused by Hypertension and Cervical Strain, respectively. Written consent from both participants has been obtained prior to the commencement of the study. We developed a gaze-based interaction game using Unity and Tobii 5’s SDK, where the participants were asked to perform the 1-out-of-8 gaze-based icon selection using the Tobii Eye Tracker 5. Each trial comprises 100 selection tasks. Each participant has performed 2 trials (1 experimental condition and 1 control condition). We have collected and analysed over 144,000 frames of video data that last around 40 minutes. Participants’ performance was measured by participant’s icon _selection time_ and _selection accuracy_ , where data was collected from the experimental condition (with adaptation) and the control condition (without adaptation) for statistical analyses. 

|||**Selection Time (s)**|**Selection Accuracy (%)**|
|---|---|---|---|
|||Mean (SD)|Mean (SD)|
||**Experimental**|4.79 (1.52)|92 (27.2)|
||**Control**|7.72 (4.32)|51 (51.1)|



Table 1: Descriptive statistics of user experiment (N = 400). 

## **Results** 

Descriptive statistics of our performance metrics are provided in Table 1. Analysis of variance (ANOVA) shows statistically significant differences across conditions in both selection time ( _p < ._ 001 _, F_ (1 _,_ 398) = 82 _._ 39) and selection accuracy ( _p < ._ 001 _, F_ (1 _,_ 398) = 103 _._ 41). Furthermore, the effect size is between small to medium for both selection time ( _η_[2] = _._ 17) and selection accuracy ( _η_[2] = _._ 21). 

## **Concluding Remarks** 

Our results show an enhancement of gazed-based interaction brought by our algorithm. Specifically, the decrease in selection time and increase in selection accuracy were both statistically significant with a small to medium effect size. Our limitations include (1) our algorithm has a lower performance when users wear glasses, (2) our head pose monitor function performs better in horizontal rather than vertical head movement. Therefore, adaption for more real-life usage scenarios needed to be developed. Also, the sample size needs to be increased in order to generalise our findings. Overall, we proposed a novel adaptation algorithm to improve the UX during gaze-based interaction, with limitations and future works briefly identified and discussed. 

## **References** 

Cruceat, A.-M.; and Butean, A. 2019. Assistive Tools for People with Cerebral Palsy: An Eye Tracker Calibration for Vision and Focus Training. In _21st SYNASC_ , 284–289. 

Karlsson, P.; Bech, A.; and Stone, H. 2019. Eyes on communication: trialling eye-gaze control technology in young children with dyskinetic cerebral palsy. _Developmental Neurorehabilitation_ , 22(2): 134–140. 

Monbaliu, E.; Himmelmann, K.; Lin, J. P.; Ortibus, E.; Bonouvri´e, L.; Feys, H.; Vermeulen, R. J.; and Dan, B. 2017. Clinical presentation and management of dyskinetic cerebral palsy. _The Lancet Neurology_ , 16: 741–749. 

Purchase, H. C. 2012. _Experimental Human-Computer Interaction: A Practical Guide with Visual Examples_ . New York: Cambridge University Press, 1st edition. 

Siniscalchi, A.; Gallelli, L.; Labate, A.; Malferrari, G.; Palleria, C.; and Sarro, G. D. 2012. Post-stroke Movement Disorders: Clinical Manifestations and Pharmacological Management. _Current Neuropharmacology_ , 10(3): 254–262. Vedaldi, A.; and et al. 2020. Towards End-to-End VideoBased Eye-Tracking. In _Computer Vision - ECCV 2020_ , volume 12357, 747–763. Switzerland: Springer. 

23670 

