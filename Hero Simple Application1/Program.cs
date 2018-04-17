using System;
using System.Threading;
using Microsoft.SPOT;
using Microsoft.SPOT.Hardware;
using CTRE;

namespace Hero_Simple_Application1
{
    public class Program
    {
        public static void Main()
        {
            CTRE.TalonSrx talon = new CTRE.TalonSrx(0);
            talon.SetControlMode(TalonSrx.ControlMode.kVoltage);
            talon.SetFeedbackDevice(TalonSrx.FeedbackDevice.CtreMagEncoder_Absolute);
            talon.SetSensorDirection(false);
            talon.SetVoltageRampRate(0.0f);

            /* simple counter to print and watch using the debugger */
            int counter = 0;
            /* loop forever */
            while (true)
            {
                /* print the three analog inputs as three columns */
                //Debug.Print("Counter Value: " + counter);
                CTRE.Watchdog.Feed();

                talon.Set(0.0f); //low ish voltage
                /* increment counter */
                ++counter; /* try to land a breakpoint here and hover over 'counter' to see it's current value.  Or add it to the Watch Tab */

                /* wait a bit */
                //using(System.IO.StreamWriter file = new System.IO.StreamWriter(@"C:\Users\Public\TestFolder\data.srv"))
                //{
                double seconds = DateTime.Now.Minute * 60 + DateTime.Now.Second + DateTime.Now.Millisecond / 1000.0;
                //CTRE.TalonSrx.VelocityMeasurementPeriod.Period_100Ms period;
                Debug.Print(seconds.ToString() + "," + talon.GetPosition().ToString() + "," + talon.GetSpeed().ToString() + "," + talon.GetOutputVoltage().ToString() + "," + talon.GetOutputCurrent().ToString());
                //talon.SetVelocityMeasurementPeriod(CTRE.TalonSrx.VelocityMeasurementPeriod.Period_10Ms);
                //  file.WriteLine(seconds.ToString() + "," + talon.GetPosition().ToString() + "," + talon.GetSpeed().ToString());
                //}
                System.Threading.Thread.Sleep(10);
            }
        }
    }
}
