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
            talon.SetFeedbackDevice(TalonSrx.FeedbackDevice.CtreMagEncoder_Relative);
            talon.SetSensorDirection(false);
            talon.SetVoltageRampRate(0.0f);
            talon.EnableCurrentLimit(false);
            talon.ConfigLimitMode(TalonSrx.LimitMode.kLimitMode_SrxDisableSwitchInputs);

            double time_per_voltage = 60;


            double[] voltages = new double[] {0,  0, 4, 0 };

            bool time_out = false;

            bool continuous = true;


            /* simple counter to print and watch using the debugger */
            int counter = 0;
            /* loop forever */
            double time_last = DateTime.Now.Hour * 3600 + DateTime.Now.Minute * 60 + DateTime.Now.Second + DateTime.Now.Millisecond / 1000.0;
            while (true)
            {
                /* print the three analog inputs as three columns */
                //Debug.Print("Counter Value: " + counter);
                CTRE.Watchdog.Feed();

				

                /* increment counter */
                ++counter; /* try to land a breakpoint here and hover over 'counter' to see it's current value.  Or add it to the Watch Tab */

                /* wait a bit */
                //using(System.IO.StreamWriter file = new System.IO.StreamWriter(@"C:\Users\Public\TestFolder\data.srv"))
                //{
                double seconds = DateTime.Now.Hour * 3600 + DateTime.Now.Minute * 60 + DateTime.Now.Second + DateTime.Now.Millisecond / 1000.0;
                UInt64 index = (UInt64)System.Math.Floor((seconds - time_last) / time_per_voltage);
                double voltage = 0;
                if (continuous)
                {
                    
                    if (index < (UInt64)voltages.Length - 1)
                    {
                        double value = (seconds - time_last) / time_per_voltage;
                        voltage = (voltages[index + 1] - voltages[index]) * (value - index) + voltages[index];
                    }
                    else if (!time_out)
                    {
                        voltage = voltages[voltages.Length - 1];
                    }

                }
                else
                {
                   
                    if (index < (UInt64)voltages.Length)
                    {
                        voltage = voltages[index];
                    }                
                    else if (!time_out)
                    {
                        voltage = voltages[voltages.Length - 1];
                    }

                }
                
				talon.Set((float)voltage); //low ish voltage
	
				//CTRE.TalonSrx.VelocityMeasurementPeriod.Period_100Ms period;
                Debug.Print(seconds.ToString() + "," + talon.GetPosition().ToString() + "," + talon.GetSpeed().ToString() + "," + talon.GetOutputVoltage().ToString() 
                    + "," + talon.GetOutputCurrent().ToString() + "," + talon.GetBusVoltage().ToString() + "," + talon.GetTemperature().ToString());
           

                //talon.SetVelocityMeasurementPeriod(CTRE.TalonSrx.VelocityMeasurementPeriod.Period_10Ms);
                //  file.WriteLine(seconds.ToString() + "," + talon.GetPosition().ToString() + "," + talon.GetSpeed().ToString());
                //}
                System.Threading.Thread.Sleep(10);
            }
        }
    }
}
