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
using BepInEx.Configuration;
using System.IO;
using System.Reflection;
using System.IO.Ports;
using HarmonyLib.Tools;
using System.Threading;
using System.Net.Sockets;
using System.Net;
using static GameObjectsToRenderTexture.Packing;
using static ColorSystem;
using UnityEngine.Rendering;
using System.Collections;

namespace MyGameMod
{
    [BepInPlugin("CursedElectricSRXD", "SpinLED", "0.1")]
    public class GameMod : BaseUnityPlugin
    {
        private static ConfigFile _config = new ConfigFile(Path.Combine(Paths.ConfigPath, "SpinLED.cfg"), true);

        public static IList<Note> noteTimer;
        public static int noteSize;

        public static string PythonData;

        public static int LEDcount { get; set; }

        public static ManualLogSource logger;

        public static int[,] LedArray = new int[450, 3];

        public static TcpListener server;

        public static string[] fruits = new string[] { "Apple", "Banana", "Cherry" };

        public static float fuck;



        private void Awake()
        {

            // Initialize logger
            logger = Logger;

            MyGameMod.SendData.Python(null);

            // Log plugin load message
            logger.LogInfo("SpinLED Sucessfully Loaded");

            // Set up Harmony patches
            var harmony = new Harmony("CursedElectricSRXD");
            harmony.PatchAll(); // Apply all patches

            // Initialize serial port

        }



        public static int Clamp(int value, int min, int max)
        {
            if (value < min) return min;
            if (value > max) return max;
            return value;
        }





        public static void awake2(Note note)
        {
            int i = 1;
            string IsBeathold = "";
            string IsHold = "";
            //logger.LogError(note.ToString());
            if (note.type == 1)
            {
                while (noteTimer[i].type != 11 && noteTimer[i].type != 1)
                {
                    i++;
                    //logger.LogError(noteTimer[i].type);
                }
                if (noteTimer[i].type == 11)
                {
                    IsBeathold = "Beatholdtrue";
                }
            }
            else
            {
                IsBeathold = "Beatholdfalse";
            }
            if (note.type == 5 || note.type == 4)
            {
                while (noteTimer[i].type != 2 && noteTimer[i].type != 3 && noteTimer[i].type != 4 && noteTimer[i].type != 12 && noteTimer[i].type != 5)
                {
                    //logger.LogError(noteTimer[i].type);
                    i++;
                }
                if (noteTimer[i].type == 5)
                {
                    IsHold = "Holdtrue";
                }
            }
            else
            {
                IsHold = "Holdfalse";
            }




            GameMod.PythonData = note.ToString() + ", " + IsBeathold + ", " + IsHold;


            // sent this fucker some trues!
            switch (note.type)
            {

                case 0:
                    // match
                    if (note.colorIndex == 1)
                    {
                        //logger.LogInfo("red match");
                        {

                            for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                                for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                                {
                                    GameMod.LedArray[a, b] += 100;

                                }
                            //Log10(LedArray);
                        }
                    }
                    else
                    {
                        //logger.LogInfo("blue match");
                        {

                            for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                                for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                                {
                                    GameMod.LedArray[a, b] += 100;

                                }
                            //Log10(LedArray);
                        }

                    }

                    break;
                case 1:
                    //beat
                    // logger.LogInfo("beat");
                    //logger.LogInfo(GameMod.LedArray.GetLength(0));
                    {

                        for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                            for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                            {
                                //LedArray[a, b] += 100;


                            }
                        //Log10(LedArray);
                    }



                    break;
                case 2:
                    //right spin
                    //logger.LogInfo("right spin");
                    {

                        for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                            for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                            {
                                GameMod.LedArray[a, b] += 100;

                            }
                        //Log10(LedArray);
                    }

                    break;
                case 3:
                    //left spin
                    //logger.LogInfo("left spin");
                    {

                        for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                            for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                            {
                                GameMod.LedArray[a, b] += 100;

                            }
                        //Log10(LedArray);
                    }

                    break;
                case 4:
                    //tap hold start
                    //logger.LogInfo("tap hold");
                    {

                        for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                            for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                            {
                                GameMod.LedArray[a, b] += 100;

                            }
                        //Log10(LedArray);
                    }

                    break;
                case 5:
                    //tap hold end
                    // logger.LogInfo("tap release");
                    {

                        for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                            for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                            {
                                GameMod.LedArray[a, b] += 100;

                            }
                        //Log10(LedArray);
                    }

                    break;
                case 8:
                    //Tappies
                    //logger.LogInfo("tap");
                    {

                        for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                            for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                            {
                                GameMod.LedArray[a, b] += 100;

                            }
                        //Log10(LedArray);
                    }

                    break;
                case 11:
                    //beathold end
                    //logger.LogInfo("beat end");
                    {

                        for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                            for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                            {
                                GameMod.LedArray[a, b] += 100;

                            }
                    }

                    break;
                case 12:
                    //scratchies
                    //logger.LogInfo("scratch note");
                    {

                        for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                            for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                            {
                                GameMod.LedArray[a, b] += 100;

                            }
                        //Log10(LedArray);
                    }

                    break;
                default:
                    //if all else fails
                    //logger.LogInfo("oopsie uwu");
                    {

                        for (int a = 0; a < GameMod.LedArray.GetLength(0); a++)
                            for (int b = 0; b < GameMod.LedArray.GetLength(1); b++)
                            {
                                GameMod.LedArray[a, b] += 100;

                            }
                        //Log10(LedArray);
                    }

                    break;


            }

        }


        [HarmonyPatch]
        public static class FindNoteData
        {
            static MethodBase TargetMethod()
            {
                var type = typeof(PlayableNoteData);

                return type.GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)
                           .Where(m => m.Name == "SetData")
                           .FirstOrDefault(m =>
                           {
                               var p = m.GetParameters();
                               return p.Length == 4 &&
                                      p[0].ParameterType.Name.Contains("IList") &&
                                      p[1].ParameterType == typeof(bool) &&
                                      p[2].ParameterType == typeof(bool) &&
                                      p[3].ParameterType.Name.Contains("TrackTick");
                           })
                       ?? throw new Exception("Correct SetData method not found!");
            }


            [HarmonyPrefix]
            public static bool Prefix(IList<Note> fromNotes, bool allowTutorialNotesIn, bool buildInvalidNoteInfoIn, object lastSustainNoteDefaultLengthArg)
            {
                //logger.LogInfo("SetData called.");

                if (fromNotes == null)
                {
                    //logger.LogError("fromNotes is null.");
                    return true;
                }

                if (fromNotes.Count == 0)
                {
                    //logger.LogError("fromNotes is empty.");
                    return true;
                }

                noteTimer = fromNotes.ToList();
                noteSize = fromNotes.Count;
                return true;
            }
        }
        



        [HarmonyPatch(typeof(PlayState), "UpdateTutorialNotes")]
        public static class FindTime
        {
            [HarmonyPrefix]
            public static bool UpdateTutorialNotes(TrackTick newCurrentTick)
            {
                if (newCurrentTick >= 0)
                {
                    double currentTimeDouble = newCurrentTick.ToSeconds();
                    float currentTime = (float)currentTimeDouble;
                }
                try
                {
                    if (noteTimer.Count > 0)
                    {
                        fuck = newCurrentTick;
                        var firstNote = noteTimer[0];
                        if (firstNote.tick < fuck + 10000)
                        {
                            fuck = newCurrentTick;
                            awake2(firstNote);
                            noteTimer.RemoveAt(0);
                        }
                    }
                }
                catch (ArgumentOutOfRangeException ex)
                {
                }

                return true;

            }


        }


    }

}
    



























