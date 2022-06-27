void tf(int c, int p)
{
int error = 0 ;
int Set = 800 ;
int Start = 0 ;
int motorSpeed;
int baseSpeed =p;
int rightSpeed, leftSpeed;
int maxSpeed = p;
int sum_error = 0;
int pre_error = 0;
int Kp= 2;
int Kd = 100;
int Ki = 0.025;

for(i=0;i<c;i++)
{
adc.begin(13, 11, 12,10 );
adc.begin(13, 11, 12,9 );
while(adc.readADC(7)<800||adc.readADC(0)<800)
{
  if (  adc.readADC(0) > Set && adc.readADC(1)<Set && adc.readADC(2)< Set && adc.readADC(3) < Set && adc.readADC(4)< Set && adc.readADC(5)< Set &&adc.readADC(6)< Set  &&  adc.readADC(7)< Set  ) {error = 7;}
  else if (  adc.readADC(0) > Set && adc.readADC(1) > Set && adc.readADC(2) < Set && adc.readADC(3) < Set && adc.readADC(4)< Set && adc.readADC(5)< Set &&adc.readADC(6)< Set  &&  adc.readADC(7)< Set  ) {error = 4;}
  else if (  adc.readADC(0) < Set && adc.readADC(1) > Set && adc.readADC(2) < Set && adc.readADC(3) < Set && adc.readADC(4) < Set && adc.readADC(5)< Set &&adc.readADC(6)< Set  &&  adc.readADC(7)< Set  ) {error = 3.5;}
  else if (  adc.readADC(0) < Set && adc.readADC(1) > Set && adc.readADC(2) > Set && adc.readADC(3) < Set && adc.readADC(4) < Set && adc.readADC(5)< Set &&adc.readADC(6)< Set  &&  adc.readADC(7)< Set  ) {error = 3;}
  else if (  adc.readADC(0) < Set &&  adc.readADC(2) > Set && adc.readADC(3) < Set && adc.readADC(4) < Set && adc.readADC(5)< Set &&adc.readADC(6)< Set  &&  adc.readADC(7)< Set  ) {error = 2.5;}
  else if (  adc.readADC(0) < Set &&  adc.readADC(2) > Set && adc.readADC(3) > Set && adc.readADC(4) < Set && adc.readADC(5) < Set &&adc.readADC(6)< Set  &&  adc.readADC(7)< Set  ) {error = 2;}
  else if (  adc.readADC(0) < Set &&  adc.readADC(2) < Set && adc.readADC(3) > Set && adc.readADC(4) < Set && adc.readADC(5)< Set &&adc.readADC(6)< Set  &&  adc.readADC(7)< Set  ) {error = 1 ;}
  else if (  adc.readADC(0) < Set &&  adc.readADC(2) < Set && adc.readADC(3) > Set && adc.readADC(4) > Set && adc.readADC(5)< Set &&adc.readADC(6)< Set  &&  adc.readADC(7) < Set  ) {error = 0 ;}
  else if (  adc.readADC(0) < Set && adc.readADC(1) <Set && adc.readADC(2) < Set && adc.readADC(3) < Set && adc.readADC(4) > Set && adc.readADC(5) < Set &&adc.readADC(6) < Set  &&  adc.readADC(7) < Set  ) {error = -1 ;}
  else if (  adc.readADC(0) < Set && adc.readADC(1)<Set && adc.readADC(2)< Set && adc.readADC(3) < Set && adc.readADC(4)> Set && adc.readADC(5)> Set &&adc.readADC(6)< Set  &&  adc.readADC(7)< Set  ) {error = -2 ;} 
  else if (  adc.readADC(0) < Set && adc.readADC(1)<Set && adc.readADC(2)< Set && adc.readADC(3) < Set && adc.readADC(4)< Set && adc.readADC(5)> Set &&adc.readADC(6)< Set  &&  adc.readADC(7)< Set  ) {error = -2.5;}
  else if (  adc.readADC(0) < Set && adc.readADC(1)<Set && adc.readADC(2)< Set && adc.readADC(3) < Set && adc.readADC(4)< Set && adc.readADC(5)> Set &&adc.readADC(6) > Set  &&  adc.readADC(7)< Set  ) {error = -3;}
  else if (  adc.readADC(0) < Set && adc.readADC(1)<Set && adc.readADC(2)< Set && adc.readADC(3) < Set && adc.readADC(4)< Set && adc.readADC(5)< Set &&adc.readADC(6)> Set  &&  adc.readADC(7)< Set  ) {error = -3.5 ;}
  else if (  adc.readADC(0) < Set && adc.readADC(1)<Set && adc.readADC(2)< Set && adc.readADC(3) < Set && adc.readADC(4)< Set && adc.readADC(5)< Set &&adc.readADC(6)> Set  &&  adc.readADC(7)> Set  ) {error = -4 ;}
  else if (  adc.readADC(0) < Set && adc.readADC(1)<Set && adc.readADC(2)< Set && adc.readADC(3) < Set && adc.readADC(4)< Set && adc.readADC(5)< Set &&adc.readADC(6)< Set  &&  adc.readADC(7)> Set  ) {error = -7 ;}
  motorSpeed = Kp * error + Kd * (error - pre_error) + Ki * (sum_error);
  rightSpeed = baseSpeed + motorSpeed;
  leftSpeed = baseSpeed - motorSpeed;
  if (leftSpeed > maxSpeed) leftSpeed = maxSpeed;
  if (rightSpeed > maxSpeed) rightSpeed = maxSpeed;
  if (leftSpeed < -maxSpeed) leftSpeed = -maxSpeed;
  if (rightSpeed < -maxSpeed) rightSpeed = -maxSpeed; 
  Motor(leftSpeed,rightSpeed); 
  pre_error = error;
  sum_error += error;
}
digitalWrite(8,1);
delay(25);
digitalWrite(8,0);

Motor(p,p);
while(analogRead(A3)>600);
}

Motorstop();
}