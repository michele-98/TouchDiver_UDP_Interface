using WeArt.Components;
using WeArt.Core;

﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WeArt.Core;
using WeArt.Components;
using WeArt.Utils;
using ClientError = WeArt.Core.WeArtClient.ErrorType;
using System.Timers;

namespace TouchDiver_Simple

{

    class deviceControl
    {

        static void Main(string[] args)
        {
            WeArtClient _weartClient;

            WeArtController weArtController = new WeArtController();
            _weartClient = weArtController.Client;

            bool isConnected = _weartClient.IsConnected;

            Console.WriteLine("Status: "+ isConnected.ToString());
            Console.ReadKey();

            _weartClient.Start();

            Console.WriteLine("START");
            Console.ReadKey();

            WeArtHapticObject hapticObject = new WeArtHapticObject(_weartClient);
            hapticObject.HandSides = HandSideFlags.Right;
            hapticObject.ActuationPoints = ActuationPointFlags.Thumb;

            Console.WriteLine("creo un effetto");
            TouchEffect touchEffect = new TouchEffect();


            // create temperature component
            Temperature temperature = Temperature.Default;
            temperature.Active = true; // must be active to work
            temperature.Value = 0.2f;

            // create force component
            Force force = Force.Default;
            force.Active = true;
            force.Value = 0.7f;

            // create texture component
            Texture texture = Texture.Default;
            texture.Active = true;
            texture.TextureType = TextureType.ProfiledAluminiumMeshFast;

            // effect set proporties 
            touchEffect.Set(temperature, force, texture);

            // add effect if needed, to thimble 
            if (hapticObject.ActiveEffect == null)
                hapticObject.AddEffect(touchEffect);

            Console.WriteLine("avviato, premi un tasto per stop");
            Console.ReadKey();
            _weartClient.Stop();


        }

    }
}