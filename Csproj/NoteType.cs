using System;

namespace MyGameMod
{

    [Flags]
    public enum NoteType
    {
        // Token: 0x04000E9B RID: 3739
        None = 0,
        // Token: 0x04000E9C RID: 3740
        Match = 1,
        // Token: 0x04000E9D RID: 3741
        DrumStart = 2,
        // Token: 0x04000E9E RID: 3742
        SpinRightStart = 4,
        // Token: 0x04000E9F RID: 3743
        SpinLeftStart = 8,
        // Token: 0x04000EA0 RID: 3744
        HoldStart = 16,
        // Token: 0x04000EA1 RID: 3745
        SectionContinuationOrEnd = 32,
        // Token: 0x04000EA2 RID: 3746
        Tap = 256,
        // Token: 0x04000EA3 RID: 3747
        Checkpoint = 512,
        // Token: 0x04000EA4 RID: 3748
        TutorialStart = 1024,
        // Token: 0x04000EA5 RID: 3749
        DrumEnd = 2048,
        // Token: 0x04000EA6 RID: 3750
        ScratchStart = 4096,
        // Token: 0x04000EA7 RID: 3751
        SpinStart = 12,
        // Token: 0x04000EA8 RID: 3752
        IsDrum = 2050,
        // Token: 0x04000EA9 RID: 3753
        IsWheel = 5949,
        // Token: 0x04000EAA RID: 3754
        UsesSectionContinuation = 4156,
        // Token: 0x04000EAB RID: 3755
        All = -1
    }
}
