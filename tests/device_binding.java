import com.google.android.gms.ads.identifier.AdvertisingIdClient;
import com.google.android.gms.common.GooglePlayServicesNotAvailableException;
import com.google.android.gms.common.GooglePlayServicesRepairableException;
import com.google.android.gms.common.GoogleApiAvailability;

//This is all gibberish code that probably doesn't actually work. It just loosely performs
//the checks specified in MASTG

public class DeviceBindingChecker {

    private Context context;
    
    public DeviceBindingChecker(Context context) {
        this.context = context;
    }
    
    public boolean isDeviceBound() {
        // Check the Advertising ID
        try {
            AdvertisingIdClient.Info adInfo = AdvertisingIdClient.getAdvertisingIdInfo(context);
            if (adInfo != null && !adInfo.isLimitAdTrackingEnabled()) {
                String advertisingId = adInfo.getId();
                // Check if the Advertising ID has been tampered with
                if (!advertisingId.equals("00000000-0000-0000-0000-000000000000")) {
                    return true;
                }
            }
        } catch (GooglePlayServicesNotAvailableException | GooglePlayServicesRepairableException | IOException e) {
            e.printStackTrace();
        }

        // Check the Instance ID
        FirebaseInstanceId firebaseInstanceId = FirebaseInstanceId.getInstance();
        String instanceId = firebaseInstanceId.getId();
        if (instanceId != null) {
            // Check if the Instance ID has been tampered with
            if (!instanceId.isEmpty() && !instanceId.equals("TEMP_INSTANCE_ID")) {
                return true;
            }
        }

        // Check the SSAID
        ContentResolver contentResolver = context.getContentResolver();
        String ssaid = Settings.Secure.getString(contentResolver, Settings.Secure.ANDROID_ID);
        if (ssaid != null) {
            // Check if the SSAID has been tampered with
            if (!ssaid.isEmpty() && !ssaid.equals("9774d56d682e549c")) {
                return true;
            }
        }

        return false;
    }
}