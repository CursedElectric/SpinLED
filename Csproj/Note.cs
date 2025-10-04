using System;
using UnityEngine;


namespace MyGameMod
{

    // Token: 0x0200029C RID: 668
    public struct Note : IEquatable<Note>
    {
        // Token: 0x06000E62 RID: 3682 RVA: 0x0004CD48 File Offset: 0x0004AF48
        public static float TicksToSeconds(long ticks)
        {
            return (float)Note.TicksToSecondsDouble(ticks);
        }

        // Token: 0x06000E63 RID: 3683 RVA: 0x0004CD51 File Offset: 0x0004AF51
        public static double TicksToSecondsDouble(long ticks)
        {
            return (double)ticks / 100000.0;
        }

        // Token: 0x06000E64 RID: 3684 RVA: 0x0004CD5F File Offset: 0x0004AF5F
        public static long SecondsToTicks(float seconds)
        {
            return Note.SecondsToTicksFromDouble((double)seconds);
        }

        // Token: 0x06000E65 RID: 3685 RVA: 0x0004CD68 File Offset: 0x0004AF68
        public static long SecondsToTicksFromDouble(double seconds)
        {
            return (long)(seconds * 100000.0);
        }

        // Token: 0x170002D4 RID: 724
        // (get) Token: 0x06000E66 RID: 3686 RVA: 0x0004CD76 File Offset: 0x0004AF76
        // (set) Token: 0x06000E67 RID: 3687 RVA: 0x0004CD7E File Offset: 0x0004AF7E
        public TrackTick tick { get; set; }

        // Token: 0x06000E68 RID: 3688 RVA: 0x0004CD88 File Offset: 0x0004AF88

        // Token: 0x06000E69 RID: 3689 RVA: 0x0004CDAC File Offset: 0x0004AFAC
        public static bool IsValidNoteType(byte type)
        {
            return Note.IsNoteTypePlaceable(type);
        }

        // Token: 0x170002D5 RID: 725
        // (get) Token: 0x06000E6A RID: 3690 RVA: 0x0004CDB4 File Offset: 0x0004AFB4
        public bool IsValid
        {
            get
            {
                return Note.IsValidNoteType(this.type);
            }
        }

        // Token: 0x06000E6B RID: 3691 RVA: 0x0004CDC1 File Offset: 0x0004AFC1
        private static bool IsNoteTypePlaceable(byte type)
        {
            return false | type == 0 | type == 1 | type == 2 | type == 3 | type == 4 | type == 5 | type == 8 | type == 11 | type == 12;
        }

        // Token: 0x170002D6 RID: 726
        // (get) Token: 0x06000E6C RID: 3692 RVA: 0x0004CDF4 File Offset: 0x0004AFF4
        // (set) Token: 0x06000E6D RID: 3693 RVA: 0x0004CE20 File Offset: 0x0004B020
        public int SpinDirection
        {
            get
            {
                byte b = this.type;
                int result;
                if (b != 2)
                {
                    if (b != 3)
                    {
                        result = 0;
                    }
                    else
                    {
                        result = 1;
                    }
                }
                else
                {
                    result = -1;
                }
                return result;
            }
            set
            {
                byte b;
                if (value >= 0)
                {
                    if (value == 0)
                    {
                        b = 0;
                    }
                    else
                    {
                        b = 3;
                    }
                }
                else
                {
                    b = 2;
                }
                this.type = b;
            }
        }

        // Token: 0x170002D7 RID: 727
        // (get) Token: 0x06000E6E RID: 3694 RVA: 0x0004CE45 File Offset: 0x0004B045
        public bool IsNormalNote
        {
            get
            {
                return this.type == 0;
            }
        }

        // Token: 0x170002D8 RID: 728
        // (get) Token: 0x06000E6F RID: 3695 RVA: 0x0004CE50 File Offset: 0x0004B050
        public bool IsColoredNote
        {
            get
            {
                return this.type == 0 || this.IsColoredNoteToHit;
            }
        }

        // Token: 0x170002D9 RID: 729
        // (get) Token: 0x06000E70 RID: 3696 RVA: 0x0004CE62 File Offset: 0x0004B062
        public bool IsDrumHit
        {
            get
            {
                return this.type == 1;
            }
        }

        // Token: 0x170002DA RID: 730
        // (get) Token: 0x06000E71 RID: 3697 RVA: 0x0004CE6D File Offset: 0x0004B06D
        public bool IsDrumHitExtension
        {
            get
            {
                return this.type == 11;
            }
        }

        // Token: 0x170002DB RID: 731
        // (get) Token: 0x06000E72 RID: 3698 RVA: 0x0004CE79 File Offset: 0x0004B079
        public bool IsSpinner
        {
            get
            {
                return this.type == 2 || this.type == 3;
            }
        }

        // Token: 0x170002DC RID: 732
        // (get) Token: 0x06000E73 RID: 3699 RVA: 0x0004CE8F File Offset: 0x0004B08F
        public bool IsFreestyleSection
        {
            get
            {
                return this.type == 4;
            }
        }

        // Token: 0x170002DD RID: 733
        // (get) Token: 0x06000E74 RID: 3700 RVA: 0x0004CE9A File Offset: 0x0004B09A
        public bool IsScratchSection
        {
            get
            {
                return this.type == 12;
            }
        }

        // Token: 0x170002DE RID: 734
        // (get) Token: 0x06000E75 RID: 3701 RVA: 0x0004CEA6 File Offset: 0x0004B0A6
        public bool IsSectionStarter
        {
            get
            {
                return this.IsSpinner || this.IsScratchSection || this.IsFreestyleSection;
            }
        }

        // Token: 0x170002DF RID: 735
        // (get) Token: 0x06000E76 RID: 3702 RVA: 0x0004CEC0 File Offset: 0x0004B0C0
        public string FreestyleEndType
        {
            get
            {
                return "";
            }

        }

        // Token: 0x170002E0 RID: 736
        // (get) Token: 0x06000E77 RID: 3703 RVA: 0x0004CEE2 File Offset: 0x0004B0E2
        public bool IsSectionContinuation
        {
            get
            {
                return this.type == 5;
            }
        }

        // Token: 0x170002E1 RID: 737
        // (get) Token: 0x06000E78 RID: 3704 RVA: 0x0004CEED File Offset: 0x0004B0ED
        public bool IsWholeBarNote
        {
            get
            {
                return this.SpinDirection != 0 || this.IsDrumHit || this.IsScratchSection || this.IsDrumHitExtension;
            }
        }

        // Token: 0x170002E2 RID: 738
        // (get) Token: 0x06000E79 RID: 3705 RVA: 0x0004CF0F File Offset: 0x0004B10F
        public bool IsColoredNoteToHit
        {
            get
            {
                return this.type == 8;
            }
        }

        // Token: 0x170002E3 RID: 739
        // (get) Token: 0x06000E7A RID: 3706 RVA: 0x0004CF1A File Offset: 0x0004B11A
        public int size
        {
            get
            {
                if (!this.IsNormalNote)
                {
                    return 2;
                }
                return 1;
            }
        }

        // Token: 0x06000E7B RID: 3707 RVA: 0x0004CF27 File Offset: 0x0004B127
        public static NoteType GetNoteTypeForCode(byte code)
        {
            return (NoteType)(1 << (int)code);
        }

        // Token: 0x06000E7C RID: 3708 RVA: 0x0004CF30 File Offset: 0x0004B130
        public static NoteType GetNoteTypeForSpinDirection(int direction)
        {
            NoteType result;
            if (direction <= 0)
            {
                if (direction >= 0)
                {
                    result = NoteType.None;
                }
                else
                {
                    result = NoteType.SpinRightStart;
                }
            }
            else
            {
                result = NoteType.SpinLeftStart;
            }
            return result;
        }

        // Token: 0x170002E4 RID: 740
        // (get) Token: 0x06000E7D RID: 3709 RVA: 0x0004CF52 File Offset: 0x0004B152
        public NoteType NoteType
        {
            get
            {
                return Note.GetNoteTypeForCode(this.type);
            }
        }

        // Token: 0x170002E5 RID: 741
        // (get) Token: 0x06000E7E RID: 3710 RVA: 0x0004CF5F File Offset: 0x0004B15F
        public bool IsAnyDrumType
        {
            get
            {
                return (this.NoteType & NoteType.IsDrum) > NoteType.None;
            }
        }

        // Token: 0x06000E7F RID: 3711 RVA: 0x0004CF70 File Offset: 0x0004B170
        public static NoteColorType ColorIndexToNoteColorType(int colorIndex)
        {
            if (colorIndex != 0)
            {
                return NoteColorType.NoteA;
            }
            return NoteColorType.NoteB;
        }

        // Token: 0x170002E6 RID: 742
        // (get) Token: 0x06000E80 RID: 3712 RVA: 0x0004CF78 File Offset: 0x0004B178
        public NoteColorType NoteColor
        {
            get
            {
                NoteColorType result = NoteColorType.Default;
                if (this.MatchesNoteType(NoteType.Match | NoteType.HoldStart | NoteType.Tap))
                {
                    result = Note.ColorIndexToNoteColorType((int)this.colorIndex);
                }
                else if (this.MatchesNoteType(NoteType.SpinLeftStart))
                {
                    result = NoteColorType.SpinLeft;
                }
                else if (this.MatchesNoteType(NoteType.SpinRightStart))
                {
                    result = NoteColorType.SpinRight;
                }
                else if (this.MatchesNoteType(NoteType.IsDrum))
                {
                    result = NoteColorType.Beat;
                }
                else if (this.MatchesNoteType(NoteType.ScratchStart))
                {
                    result = NoteColorType.Scratch;
                }
                return result;
            }
        }

        // Token: 0x06000E81 RID: 3713 RVA: 0x0004CFDD File Offset: 0x0004B1DD
        public bool MatchesNoteType(NoteType noteType)
        {
            return (this.NoteType & noteType) > NoteType.None;
        }

        // Token: 0x06000E82 RID: 3714 RVA: 0x0004CFEC File Offset: 0x0004B1EC
        

        // Token: 0x06000E83 RID: 3715 RVA: 0x0004D05F File Offset: 0x0004B25F

        // Token: 0x06000E84 RID: 3716 RVA: 0x0004D070 File Offset: 0x0004B270
        public bool Equals(Note other)
        {
            return this.type == other.type && this.tick == other.tick && this.unfilteredSize == other.unfilteredSize && this.column == other.column && this.colorIndex == other.colorIndex;
        }

        // Token: 0x06000E85 RID: 3717 RVA: 0x0004D0D0 File Offset: 0x0004B2D0
        public override string ToString()
        {
            string text = this.NoteType.ToString();
            string result;
            if (this.IsColoredNote || this.IsFreestyleSection)
            {
                string text2 = (this.colorIndex == 0) ? "Blue" : "Red";
                result = string.Format("{0} {1} ({2}) at {3:0.0}", new object[]
                {
                    text2,
                    text,
                    this.column,
                    this.tick.ToSecondsFloat()
                });
            }
            else
            {
                result = string.Format("{0} at {1}", text, this.tick.ToSecondsFloat());
            }
            return result;
        }

        // Token: 0x04000EB6 RID: 3766
        public const long TicksPerSecond = 100000L;

        // Token: 0x04000EB7 RID: 3767
        public const long TicksPerTenths = 10000L;

        // Token: 0x04000EB8 RID: 3768
        public const long TicksPerHundredths = 1000L;

        // Token: 0x04000EB9 RID: 3769
        public const long TicksPerMillisecond = 100L;

        // Token: 0x04000EBA RID: 3770
        public const long TicksPerDateTick = 100L;

        // Token: 0x04000EBC RID: 3772
        public byte type;

        // Token: 0x04000EBD RID: 3773
        public byte colorIndex;

        // Token: 0x04000EBE RID: 3774
        public sbyte column;

        // Token: 0x04000EBF RID: 3775
        public byte unfilteredSize;

        // Token: 0x04000EC0 RID: 3776
        public const int NormalNoteCode = 0;

        // Token: 0x04000EC1 RID: 3777
        public const int DrumStartCode = 1;

        // Token: 0x04000EC2 RID: 3778
        public const int NegativeSpinCode = 2;

        // Token: 0x04000EC3 RID: 3779
        public const int PositiveSpinCode = 3;

        // Token: 0x04000EC4 RID: 3780
        public const int FreestyleSectionStart = 4;

        // Token: 0x04000EC5 RID: 3781
        public const int SectionContinuationCode = 5;

        // Token: 0x04000EC6 RID: 3782
        public const int ColoredNoteToHit = 8;

        // Token: 0x04000EC7 RID: 3783
        public const int DrumEndCode = 11;

        // Token: 0x04000EC8 RID: 3784
        public const int ScratchSectionStartCode = 12;

        // Token: 0x04000EC9 RID: 3785
        public const int TypeCount = 13;

        // Token: 0x0200029D RID: 669
        [Serializable]
        public struct OriginalFormat
        {

            // Token: 0x170002E7 RID: 743
            // (get) Token: 0x06000E87 RID: 3719 RVA: 0x0004D1D8 File Offset: 0x0004B3D8
            public Note Note
            {
                get
                {
                    return new Note
                    {
                        tick = Note.SecondsToTicks(this.time),
                        type = this.type,
                        colorIndex = this.colorIndex,
                        column = this.column,
                        unfilteredSize = this.m_size
                    };
                }
            }

            // Token: 0x06000E88 RID: 3720 RVA: 0x0004D23C File Offset: 0x0004B43C
            public OriginalFormat(Note note)
            {
                this.time = Note.TicksToSeconds(note.tick);
                this.type = note.type;
                this.colorIndex = note.colorIndex;
                this.column = note.column;
                this.m_size = note.unfilteredSize;
            }

            // Token: 0x04000ECA RID: 3786
            [SerializeField]
            public float time;

            // Token: 0x04000ECB RID: 3787
            public byte type;

            // Token: 0x04000ECC RID: 3788
            public byte colorIndex;

            // Token: 0x04000ECD RID: 3789
            public sbyte column;

            // Token: 0x04000ECE RID: 3790
            public byte m_size;
        }

        // Token: 0x0200029E RID: 670
        [Serializable]
        public struct BinaryFormat : IEquatable<Note.BinaryFormat>
        {
            // Token: 0x170002E8 RID: 744
            // (get) Token: 0x06000E89 RID: 3721 RVA: 0x0004D290 File Offset: 0x0004B490
            public Note Note
            {
                get
                {
                    return new Note
                    {
                        tick = (long)this.tk,
                        type = this.tp,
                        colorIndex = this.c,
                        column = this.p,
                        unfilteredSize = this.s
                    };
                }
            }

            // Token: 0x06000E8A RID: 3722 RVA: 0x0004D2F0 File Offset: 0x0004B4F0
            public BinaryFormat(Note note)
            {
                this.tk = (int)note.tick;
                this.tp = note.type;
                this.c = note.colorIndex;
                this.p = note.column;
                this.s = note.unfilteredSize;
            }

            // Token: 0x06000E8B RID: 3723 RVA: 0x0004D340 File Offset: 0x0004B540
            public bool Equals(Note.BinaryFormat other)
            {
                return this.tk == other.tk && this.tp == other.tp && this.c == other.c && this.p == other.p && this.s == other.s;
            }

            // Token: 0x06000E8C RID: 3724 RVA: 0x0004D398 File Offset: 0x0004B598
            public override bool Equals(object obj)
            {
                if (obj is Note.BinaryFormat)
                {
                    Note.BinaryFormat other = (Note.BinaryFormat)obj;
                    return this.Equals(other);
                }
                return false;
            }

            // Token: 0x06000E8D RID: 3725 RVA: 0x0004D3BD File Offset: 0x0004B5BD

            // Token: 0x04000ECF RID: 3791
            public int tk;

            // Token: 0x04000ED0 RID: 3792
            public byte tp;

            // Token: 0x04000ED1 RID: 3793
            public byte c;

            // Token: 0x04000ED2 RID: 3794
            public sbyte p;

            // Token: 0x04000ED3 RID: 3795
            public byte s;
        }
    }
}