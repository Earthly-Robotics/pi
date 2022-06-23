#include <AX12A.h>
#include <SoftwareSerial.h>
#include <stdio.h>

#define DirectionPin (5u)
#define BaudRate (1000000ul)

#define MAGNET (22)      // magnet servo
#define HOPPER (1)       // hopper servo
#define ARM (69)         // arm servo
#define RIGHT_WHEEL (61) // right wheel servo
#define LEFT_WHEEL (10)  // left wheel servo
#define BACK_WHEEL (144) // back wheel servo

String msg;
SoftwareSerial softwareSerial(16, 15);

// middle point of servo in degrees and decimal
int initial_pos = 512;
int initial_deg = 150;

// initialisation for reading inputs
String servo;
int id;
int graden;
String command;
String returnString = "";

// standard speed value
int speed = 200;

// start setup
void setup()
{
  softwareSerial.begin(9600);
  ax12a.begin(BaudRate, DirectionPin, &Serial);
  ax12a.setEndless(HOPPER, ON);
}

// start loop
void loop()
{
  readSerialPort();
  softwareSerial.flush();
  if(returnString != "")
  {
    softwareSerial.print(returnString);
  }
    returnString = "";
  delay(500);
}

// Read messages that come in through the serial port
void readSerialPort()
{
  msg = "";
  while (softwareSerial.available() > 0)
  {
    delay(10);
    char input = (char)softwareSerial.read();
    if (softwareSerial.available() == 0){
        msg += input;
    }
    if (input == '~' || softwareSerial.available() == 0)
    {
        moveServo();
        msg = "";
        continue;
    }
    msg += input;
  }
}

// The servo is only able to turn 300 degrees, the middle is 150 degrees
// The function calculates the decimal it has to turn from the middle based on the degrees given
int convertDegrees(int extra_deg)
{
  long wanted_deg = initial_deg + extra_deg;
  int result = floor((wanted_deg * initial_pos) / initial_deg);

  return result;
}

// gets the input string and splits it with the ; as a seperator
void splitString()
{
  int index = msg.indexOf(';');
  servo = msg.substring(0, index);
  String input2 = msg.substring(index + 1, msg.length());

  if (servo == "hopper")
  {
    speed = input2.toInt();
  }
  else
  {
    graden = input2.toInt();
  }
}

void moveServo()
{
    splitString();
    returnString += " STARTING SERVO MOVEMENT ";
    // Initialise the right id based on the string that was given
    if (servo == "hopper")
    {
      id = HOPPER;
      returnString += "hopper";
    }
    else if (servo == "magnet")
    {
      id = MAGNET;
      returnString += "magnet";
    }
    else if (servo == "arm")
    {
      id = ARM;
      returnString += "arm";
    }
    else if (servo == "right_wheel")
    {
      id = RIGHT_WHEEL;
      returnString += "right wheel";
    }
    else if (servo == "left_wheel")
    {
      id = LEFT_WHEEL;
      returnString += "left_wheel";
    }
    else if (servo == "back_wheel")
    {
      id = BACK_WHEEL;
      returnString += "back wheel";
    }
    else
    {
    returnString += " Servo not recognized ";
    returnString += servo;
      return;
    }
    returnString += " ID = ";
    returnString += String(id);

    // If there are degrees given move servo to the given degrees
    if (servo == "hopper")
    {
      // make spin
        returnString += " SPINNING THE HOPPER SPEED: ";
        returnString += String(speed);
        ax12a.turn(id, LEFT, speed);
        delay(500);
        ax12a.turn(id, LEFT, 0);
        return;
    }
    else if (graden != NULL)
    {
      // servo is not allowed to turn further than than 30 deg both ways
      if (servo == "magnet")
      {
        if (graden > 30 || graden < -30)
        {
            returnString += " Graden was ";
            returnString += String(graden);
            returnString += " which is not between the bounds -30 and 30";
          return;
        }
      }
      else if (servo == "back_wheel")
      {
        graden += 40;
      }
      else if (servo == "right_wheel")
      {
        graden *= -1;
      }
        returnString += " Graden was ";
        returnString += String(graden);
        ax12a.move(id, convertDegrees(graden));
    }
    else if (graden == 0)
    {
      graden = 512;
      if (servo == "back_wheel")
      {
        graden = convertDegrees(40);
      }
        returnString += " Graden was NUL: ";
        returnString += String(graden);
        ax12a.move(id, graden);
    }
    else
    {
        returnString += "SOMETHING WENT WRONG!";
    }
}
