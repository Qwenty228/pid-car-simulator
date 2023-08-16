# PID car simulator
A proportional–integral–derivative controller (PID controller or three-term controller) is a control loop mechanism employing feedback that is widely used in industrial control systems and a variety of other applications requiring continuously modulated control.

In this simulation, PID is used to control the speed of each side of the car(tank steerimg system) by using the distance between the car and wall as the 'error'.

<!-- https://user-images.githubusercontent.com/68010275/175910885-4e553675-5ced-493a-84be-5d449cd8ea18.mp4 -->

<h3><i>PID Car</i></h3>
<img src="https://user-images.githubusercontent.com/68010275/176211568-e0b61f76-09e8-48ee-b329-f57ab7a1646f.gif">

<h3><i>PID Car w/ debug</i></h3>
<div><img src="https://user-images.githubusercontent.com/68010275/176211579-45df970b-770f-47a5-979f-cd4ee1183335.gif"></div>

<div><img src="https://user-images.githubusercontent.com/68010275/176230254-b7059e64-ae40-4fdd-9087-4e3c94422135.gif"></div>


<p>
<div><big><bold>Conclusion 29-6-2022</big></bold></div>
<div>Error is the different between distances of 2 car front sensors and wall. </div>
<div>More P results in large angle change.</div>
<div>More I results in less turning radius (residual error in this case is the turning radius).</div>
<div>More D results in less oscillation.</div>
</p>

<img src="https://user-images.githubusercontent.com/68010275/176249387-49688cc7-1626-497f-aa76-383fa5a85822.gif">
