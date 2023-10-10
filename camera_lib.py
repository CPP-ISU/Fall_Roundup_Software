import serial

class camera():
    def __init__(self,com_port):
        self.cam_ser=serial.Serial(com_port,38400,8,"N",1,1)
        self.address=1

    def send_cmd(self,cmd_str):
        command=bytes.fromhex(cmd_str)
        self.cam_ser.write(command)
        response=self.cam_ser.read(10)
        return response
    
    def move(self,pan_speed,tilt_speed):
        pc=3
        if pan_speed>0:
            pc=2
        elif pan_speed<0:
            pc=1
        tc=3
        if tilt_speed>0:
            tc=2
        elif tilt_speed<0:
            tc=1
        pan_speed=abs(pan_speed)
        tilt_speed=abs(tilt_speed)


        command=f"8{self.address} 01 06 01 {format(pan_speed, '02x')} {format(tilt_speed, '02x')} 0{pc} 0{tc} FF"
        print(command)
        result=self.send_cmd(command)
        print(result)
    
    def abs_pos(self,pan_speed,tilt_speed,pan_pos,tilt_pos):
        command=f"{self.address} 01 06 02 {format(pan_speed, '02x')} 00 0"


if __name__=="__main__":
    cam=camera("COM4")
    for i in range(1):
        cam.move(-13,-13)
    cam.cam_ser.close()