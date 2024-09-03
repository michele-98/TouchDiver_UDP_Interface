using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WeArt.Core;
using WeArt.Components;
using WeArt.Utils;
using ClientError = WeArt.Core.WeArtClient.ErrorType;
using System.Timers;

namespace touchDiverCS
{

    public class DeviceControl
    {
                
        private WeArtClient _weartClient;
        private WeArtController weArtController;
        private WeArtHapticObject hapticObject;
        private TouchEffect touchEffect;
        public event Action OnUpdate;


        private void CreateClient()
        {

            // create WEART Controller
            weArtController = new WeArtController();
            _weartClient = weArtController.Client;
        }
        private void StartClient()
        {
            _weartClient.Start();

        }


        private void CreateHapticObjects()
        {
            hapticObject = new WeArtHapticObject(_weartClient);
            hapticObject.HandSides = HandSideFlags.Right;
            hapticObject.ActuationPoints = ActuationPointFlags.Thumb;

        }


        public void Initialize() {

            CreateClient();
            StartClient();
            CreateHapticObjects();
        }


        public void SetTouchEffect(float temperature_value, float force_value, int texture_id, int texture_volume)
        {
            // create temperature component
            Temperature temperature = Temperature.Default;
            temperature.Active = true; // must be active to work
            temperature.Value = temperature_value;

            // create force component
            Force force = Force.Default;
            force.Active = true;
            force.Value = force_value;

            // create texture component
            Texture texture = Texture.Default;
            texture.Active = true;
            texture.TextureType = (TextureType)texture_id;
            if (texture_volume > 100)
            {
                texture_volume = 100;
            }
            texture.Volume = texture_volume;
                

            // effect set proporties 
            touchEffect.Set(temperature, force, texture);

            // add effect if needed, to thimble 
            if (hapticObject.ActiveEffect == null)
                hapticObject.AddEffect(touchEffect);
        }


        public void createTouchEffect()
        {
            touchEffect = new TouchEffect();
            // create temperature component
            Temperature temperature = Temperature.Default;
            temperature.Active = false; // must be active to work
            temperature.Value = 0.5f;

            // create force component
            Force force = Force.Default;
            force.Active = false;
            force.Value = 0f;

            // create texture component
            Texture texture = Texture.Default;
            texture.Active = false;
            texture.TextureType = TextureType.ProfiledAluminiumMeshFast;

            // effect set proporties 
            touchEffect.Set(temperature, force, texture);

            // add effect if needed, to thimble 
            if (hapticObject.ActiveEffect == null)
                hapticObject.AddEffect(touchEffect);

        }

        public void updateTouchEffect()
        {
            OnUpdate?.Invoke();


        }

        public void stopClient() 
        {
            _weartClient.Stop();

        }






    }
}
