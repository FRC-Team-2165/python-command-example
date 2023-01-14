import wpilib
from wpilib.drive import MecanumDrive
import commands2
import navx
import rev

class DriveSubsystem(commands2.SubsystemBase):
    frontLeft: rev.CANSparkMax
    frontRight: rev.CANSparkMax
    rearLeft: rev.CANSparkMax
    rearRight: rev.CANSparkMax

    drive_train: MecanumDrive

    gyro: navx.AHRS

    def __init__(self, frontLeft: int, frontRight: int, rearLeft: int, rearRight: int) -> None:
        self.frontLeft = rev.CANSparkMax(frontLeft, rev.CANSparkMax.MotorType.kBrushless)
        self.frontRight = rev.CANSparkMax(frontRight, rev.CANSparkMax.MotorType.kBrushless)
        self.rearLeft = rev.CANSparkMax(rearLeft, rev.CANSparkMax.MotorType.kBrushless)
        self.rearRight = rev.CANSparkMax(rearRight, rev.CANSparkMax.MotorType.kBrushless)

        self.drive_train = MecanumDrive(frontLeft, frontRight, rearLeft, rearRight)

        self.gyro = navx.AHRS(wpilib.SPI.Port.kMXP)

        # This is super important. This calls SubsystemBase's constructor, which sets up DriveSubsystem 
        # as an actual subsystem, according to wpilib. Otherwise this is just a class that doesn't 
        # really do anything.
        super.__init__()

    def drive(self, x_speed: int, y_speed: int, rot: int) -> None:
        # Here we are invoking the MecanumDrive's own drive method, since we don't need to 
        # reinvent the wheel.
        self.drive_train.driveCartesian(x_speed, y_speed, rot)

    def fullstop(self) -> None:
        # This completely stops all motion on the robot, which is useful, since without 
        # telling it to stop, the robot will just keep driving.
        self.drive_train.stopMotor()

    def angle(self) -> float:
        # Get the Yaw angle from the gyro (rotation around Z-axis).
        return self.gyro.getAngle()

    def reset(self) -> None:
        # Set the gyro's current angle to zero.
        self.gyro.zeroYaw()
    