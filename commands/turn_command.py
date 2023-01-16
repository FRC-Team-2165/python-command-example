import commands2

from subsystems.drive import DriveSubsystem

class TurnCommand(commands2.CommandBase):
    drive: DriveSubsystem
    target_angle: float

    def __init__(self, subsystem: DriveSubsystem, angle: float) -> None:
        # This is important. If you don't call this, you can't register any requirements, and 
        # things will break in very weird ways.
        super().__init__()
        self.drive = subsystem

        self.target_angle = angle
        # Don't forget to register the subsystem with the command
        self.addRequirements(self.drive)

    def initialize(self) -> None:
        # We want to reset the gyro, so we aren't starting off from an unknown angle.
        # If we don't, we could already be past the angle, and this will do nothing, or 
        # we may turn farther than we want.
        self.drive.reset()
    
    def execute(self) -> None:
        # When we're running this command, we will turn clockwise at 40% speed. This is 
        # arbitrary and can absolutely be different for other commands. This speed can 
        # even by dynamically calculated.
        self.drive.drive(0, 0, 0.2)
    
    def end(self, interrupted: bool) -> None:
        # When we're done running this command, we want to stop spinning. Maybe we want
        # to keep driving when the command is over, but maybe not. We let some other command
        # figure that out.
        self.drive.fullstop()

    def isFinished(self) -> bool:
        # We only want to stop if we've rotated up to or past the target angle.
        return self.drive.angle() >= self.target_angle
