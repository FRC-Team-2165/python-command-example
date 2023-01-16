import wpilib
import commands2

from subsystems.drive import DriveSubsystem

class DriveCommand(commands2.CommandBase):
    drive_subsystem: DriveSubsystem
    controller: wpilib.XboxController

    def __init__(self, subsystem: DriveSubsystem, controller: wpilib.XboxController):
        # This is important. If you don't call this, you can't register any requirements, and 
        # things will break in very weird ways.
        super().__init__()
        
        # Store these values so we have a reference to them later.
        self.drive_subsystem = subsystem
        self.controller = controller

        # Make sure to add this as a requirement, otherwise it may conflict with other
        # commands that use the same subsystem.
        self.addRequirements(self.drive_subsystem)
    
    def initialize(self) -> None:
        # No need to do anything here, since driving is constant
        pass

    def execute(self) -> None:
        # Get our values from the controller. We can't just pass these in as arguments
        # because we won't actually call this function ourselves.
        x = self.controller.getLeftX()
        y = -self.controller.getLeftY()
        rot = self.controller.getRightX()

        # Pass our controller values into the drive subsystem, and let it handle them,
        # however it does so.
        self.drive_subsystem.drive(x, y, rot)

    def end(self, interrupted: bool) -> None:
        # The command should never end, so this should never be called
        pass

    
    def isFinished(self) -> bool:
        # We want this command to run forever
        return False