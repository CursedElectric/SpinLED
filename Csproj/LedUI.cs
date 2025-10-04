using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SpinPlayerValueStores;
using SpinCore.Translation;
using SpinCore.UI;
using SpinCore.Utility;
using BepInEx;
using static GameplayVariables;
using static GameStateConfig;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;
using XDMenuPlay.Customise;
using XDMenuPlay;
using Object = UnityEngine.Object;
using System.Runtime.InteropServices;
using static TutorialMessage;
using BepInEx.Logging;
using HarmonyLib;


namespace MyGameMod
{
    public static class SpinLEDUI
    {
        public static int LEDcount { get; set; }

        private static GameObject _ButtonBase;

        private static CustomGroup _SpinLED;
        public static void Initialize()
        {
            var page = UIHelper.CreateCustomPage("SpinLED");
            page.OnPageLoad += pageParent =>
            {
                
                    var group = UIHelper.CreateGroup(pageParent, "General Settings");
                    UIHelper.CreateSectionHeader(
                        group.Transform,
                        "General Header",
                        "SpinLED_ModSettings_GeneralHandler",
                        true
                        );

                    UIHelper.CreateLargeMultiChoiceButton(
                            group.Transform,
                            //group transform
                            "LED Count",
                            //string name. what it says in game? 
                            "SpinLED_ModSettings_LEDcount",
                            //name in config file?
                            (int)(SpinLEDUI.LEDcount),
                            //unsure
                            SpinLED,
                            //REALLY unsure
                            () => new IntRange(1, 1001),
                            //range of slider
                            v => v.ToString()
                            );

                
            };                
                UIHelper.RegisterMenuInModSettingsRoot("SpinLED_ModSettings_LEDcount", page);
            

        }


        internal static void SpinLED(int value)
        {
            LEDcount = value;
        }
    }
}

