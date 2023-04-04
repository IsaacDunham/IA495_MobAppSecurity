import android.app.Activity;
import android.app.KeyguardManager;
import android.content.Context;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Insert provided code here
        KeyguardManager mKeyguardManager = (KeyguardManager) getSystemService(Context.KEYGUARD_SERVICE);
        if (!mKeyguardManager.isKeyguardSecure()) {
            TextView lockScreenStatusTextView = findViewById(R.id.lockScreenStatusTextView);
            lockScreenStatusTextView.setText("Please set a lock screen for your device!");
        }

        TextView lockScreenStatusTextView = findViewById(R.id.lockScreenStatusTextView);

        KeyguardManager keyguardManager = (KeyguardManager) getSystemService(Context.KEYGUARD_SERVICE);

        if(keyguardManager.isKeyguardSecure()) {
            lockScreenStatusTextView.setText("Lock screen is enabled");
        } else {
            lockScreenStatusTextView.setText("Lock screen is not enabled");
        }
    }
}