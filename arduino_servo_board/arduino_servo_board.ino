#include <Servo.h>

Servo sv_fl_hip_z;
Servo sv_fl_hip_y;
Servo sv_fl_knee;

Servo sv_fr_hip_z;
Servo sv_fr_hip_y;
Servo sv_fr_knee;

Servo sv_bl_hip_z;
Servo sv_bl_hip_y;
Servo sv_bl_knee;

Servo sv_br_hip_z;
Servo sv_br_hip_y;
Servo sv_br_knee;


//servos for front left leg
#define SV_FL_HIP_Z 2
#define SV_FL_HIP_Y 3
#define SV_FL_KNEE 4

//servos for front right leg
#define SV_FR_HIP_Z 5
#define SV_FR_HIP_Y 6
#define SV_FR_KNEE 7

//servos for back left leg
#define SV_BL_HIP_Z 8
#define SV_BL_HIP_Y 9
#define SV_BL_KNEE 10

//servos for back right leg
#define SV_BR_HIP_Z 11
#define SV_BR_HIP_Y 12
#define SV_BR_KNEE 13

String data;
int index = -1;
int servo_pin = 0;
int servo_position = 0;


void setup() 
{
  Serial.begin(115200);
  Serial.setTimeout(1); 

  sv_fl_hip_z.attach(SV_FL_HIP_Z);
  sv_fl_hip_y.attach(SV_FL_HIP_Y);
  sv_fl_knee.attach(SV_FL_KNEE);

  sv_fr_hip_z.attach(SV_FR_HIP_Z);
  sv_fr_hip_y.attach(SV_FR_HIP_Y);
  sv_fr_knee.attach(SV_FR_KNEE);

  sv_bl_hip_z.attach(SV_BL_HIP_Z);
  sv_bl_hip_y.attach(SV_BL_HIP_Y);
  sv_bl_knee.attach(SV_BL_KNEE);

  sv_br_hip_z.attach(SV_BR_HIP_Z);
  sv_br_hip_y.attach(SV_BR_HIP_Y);
  sv_br_knee.attach(SV_BR_KNEE);
  
}


void loop()
{
  //continuous loop waiting until connection is made
  while (!Serial.available());

  //data in format "pin/position"
  data = Serial.readString();

  //find index of split between pin and position
  index = data.indexOf('/');

  if (index > -1)
  {
    servo_pin = data.substring(0, index).toInt();
    servo_position = data.substring(index + 1).toInt();

    switch(servo_pin)
    {
      case SV_FL_HIP_Z:
        sv_fl_hip_z.write(servo_position);
        break;

      case SV_FL_HIP_Y:
        sv_fl_hip_y.write(servo_position);
        break;

      case SV_FL_KNEE:
        sv_fl_knee.write(servo_position);
        break;


      case SV_FR_HIP_Z:
        sv_fr_hip_z.write(servo_position);
        break;

      case SV_FR_HIP_Y:
        sv_fr_hip_y.write(servo_position);
        break;

      case SV_FR_KNEE:
        sv_fr_knee.write(servo_position);
        break;


      case SV_BL_HIP_Z:
        sv_bl_hip_z.write(servo_position);
        break;

      case SV_BL_HIP_Y:
        sv_bl_hip_y.write(servo_position);
        break;

      case SV_BL_KNEE:
        sv_bl_knee.write(servo_position);
        break;


      case SV_BR_HIP_Z:
        sv_br_hip_z.write(servo_position);
        break;

      case SV_BR_HIP_Y:
        sv_br_hip_y.write(servo_position);
        break;

      case SV_BR_KNEE:
        sv_br_knee.write(servo_position);
        break;

    }
    
  }

}