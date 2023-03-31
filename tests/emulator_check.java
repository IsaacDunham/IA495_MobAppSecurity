import android.content.Context;
import android.os.Bundle;
import android.telephony.TelephonyManager;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

//This is all gibberish code that probably doesn't actually work. It just loosely performs
//the checks specified in MASTG

public class EmulatorDetector {

    public static void detectEmulator(Context context) {
        TelephonyManager telephonyManager = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
        String simSerialNumber = telephonyManager.getSimSerialNumber();
        String line1Number = telephonyManager.getLine1Number();
        String deviceId = telephonyManager.getDeviceId();
        String subscriberId = telephonyManager.getSubscriberId();
        String voiceMailNumber = telephonyManager.getVoiceMailNumber();

        if ((simSerialNumber != null && simSerialNumber.equals("89014103211118510720"))
                || (line1Number != null && line1Number.equals("155552155"))
                || (deviceId != null && (deviceId.equals("0") || deviceId.equals("000000000000000")))
                || (subscriberId != null && subscriberId.equals("310260000000000"))
                || (voiceMailNumber != null && voiceMailNumber.equals("15552175049"))) {
            Toast.makeText(context, "This app is being run on an emulator!", Toast.LENGTH_LONG).show();
        }
    }
}
