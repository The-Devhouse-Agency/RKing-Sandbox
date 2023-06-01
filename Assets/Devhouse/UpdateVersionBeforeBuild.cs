using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
#endif

namespace Devhouse.Tools.Automation
{
    public class UpdateVersionBeforeBuild : MonoBehaviour // ***TEMP REMOVE FOR BUILD ISSUES***  , IPreprocessBuildWithReport
    {
        /*
        public int callbackOrder { get { return 0; } }
        public void OnPreprocessBuild(BuildReport report)
        {
            string versionNumber = PlayerSettings.bundleVersion;
            List<string> versionParts = new List<string>(versionNumber.Split("."));
            //int toIncrement = Int32.Parse(versionParts[versionParts.Count - 1]);
            //versionParts.RemoveAt(versionParts.Count - 1);
            //string newVersionNumber = "";

            //foreach(string part in versionParts)
            //{
            //    newVersionNumber += part + ".";
            //}

            //toIncrement++;
            //newVersionNumber += toIncrement;

            //////////////////

            //Version number should be formatted as follows: 1.0.0.0 Ex: 3.5.52.534
            //versionNumber = PlayerSettings.bundleVersion;
            //versionParts = new List<string>(versionNumber.Split("."));

            //TODO: need error handling for input validation
            Debug.Log(versionParts.Count);
            GameInfo info;
            if (versionParts.Count == 4)
            {
                info = new GameInfo(Int32.Parse(versionParts[0]), Int32.Parse(versionParts[1]), Int32.Parse(versionParts[2]), Int32.Parse(versionParts[3]));

                info.versionBuild += 1;
                PlayerSettings.bundleVersion = info.VersionNumberAsString();

                string infoAsJson = JsonUtility.ToJson(info);
                Debug.Log(infoAsJson);
                File.WriteAllText("Assets/Resources/version.txt", infoAsJson);
            }
            else
            {
                Debug.Log("Wrong version number format. Only has " + versionParts.Count + " parts.");
            }
            
            //////////////////
                
            //PlayerSettings.bundleVersion = newVersionNumber;
        }
    }

    [System.Serializable]
    public class GameInfo
    {
        public int versionMajor;

        public int versionMinor;

        public int versionCommit;

        public int versionBuild;

        public GameInfo()
        {
            versionMajor = 1;
            versionMinor = 0;
            versionCommit = 0;
            versionBuild = 0;
        }

        public GameInfo(int major, int minor, int commit, int build)
        {
            versionMajor = major;
            versionMinor = minor;
            versionCommit = commit;
            versionBuild = build;
        }

        public string VersionNumberAsString()
        {
            return versionMajor + "." + versionMinor + "." + versionCommit + "." + versionBuild;
        }*/
    }
}
