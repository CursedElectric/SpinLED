using System;


namespace MyGameMod
{

    // Token: 0x02000299 RID: 665
    public struct TrackTick : IComparable<TrackTick>, IEquatable<TrackTick>
    {
        // Token: 0x170002CE RID: 718
        // (get) Token: 0x06000E29 RID: 3625 RVA: 0x0004C6F1 File Offset: 0x0004A8F1
        // (set) Token: 0x06000E2A RID: 3626 RVA: 0x0004C6F9 File Offset: 0x0004A8F9
        public long LongValue
        {
            get
            {
                return this.value;
            }
            set
            {
                this.value = value;
            }
        }

        // Token: 0x170002CF RID: 719
        // (get) Token: 0x06000E2C RID: 3628 RVA: 0x0004C736 File Offset: 0x0004A936
        public static TrackTick CloseNoteRange
        {
            get
            {
                return TrackTick.OneSemisecond;
            }
        }

        // Token: 0x170002D0 RID: 720
        // (get) Token: 0x06000E2D RID: 3629 RVA: 0x0004C73D File Offset: 0x0004A93D
        public static TrackTick MaxValue
        {
            get
            {
                return new TrackTick(long.MaxValue);
            }
        }

        // Token: 0x170002D1 RID: 721
        // (get) Token: 0x06000E2E RID: 3630 RVA: 0x0004C74D File Offset: 0x0004A94D
        public static TrackTick MinValue
        {
            get
            {
                return new TrackTick(long.MinValue);
            }
        }

        // Token: 0x06000E2F RID: 3631 RVA: 0x0004C6F9 File Offset: 0x0004A8F9
        public TrackTick(long a)
        {
            this.value = a;
        }

        // Token: 0x06000E30 RID: 3632 RVA: 0x0004C6F1 File Offset: 0x0004A8F1
        public static implicit operator long(TrackTick a)
        {
            return a.value;
        }

        // Token: 0x06000E31 RID: 3633 RVA: 0x0004C760 File Offset: 0x0004A960
        public static implicit operator TrackTick(long a)
        {
            return new TrackTick
            {
                value = a
            };
        }

        // Token: 0x06000E32 RID: 3634 RVA: 0x0004C77E File Offset: 0x0004A97E
        public static TrackTick operator +(TrackTick a, TrackTick b)
        {
            return a.value + b.value;
        }

        // Token: 0x06000E33 RID: 3635 RVA: 0x0004C792 File Offset: 0x0004A992
        public static TrackTick operator -(TrackTick a, TrackTick b)
        {
            return a.value - b.value;
        }

        // Token: 0x06000E34 RID: 3636 RVA: 0x0004C7A6 File Offset: 0x0004A9A6
        public double ToSeconds()
        {
            return Note.TicksToSecondsDouble(this.value);
        }

        // Token: 0x06000E35 RID: 3637 RVA: 0x0004C7B3 File Offset: 0x0004A9B3
        public float ToSecondsFloat()
        {
            return Note.TicksToSeconds(this.value);
        }

        // Token: 0x06000E36 RID: 3638 RVA: 0x0004C7C0 File Offset: 0x0004A9C0
        public static TrackTick FromMilliseconds(long milliseconds)
        {
            return 100L * milliseconds;
        }

        // Token: 0x06000E37 RID: 3639 RVA: 0x0004C7CC File Offset: 0x0004A9CC
        public static TrackTick FromDateTicks(long dateTicks)
        {
            return dateTicks / 100L;
        }

        // Token: 0x06000E38 RID: 3640 RVA: 0x0004C7D8 File Offset: 0x0004A9D8
        public static TrackTick FromTimeSpan(TimeSpan timeSpan)
        {
            return TrackTick.FromDateTicks(timeSpan.Ticks);
        }

        // Token: 0x06000E39 RID: 3641 RVA: 0x0004C7E6 File Offset: 0x0004A9E6
        public long ToMilliseconds()
        {
            return this.value / 100L;
        }

        // Token: 0x06000E3A RID: 3642 RVA: 0x0004C7F2 File Offset: 0x0004A9F2
        public static TrackTick FromSeconds(double seconds)
        {
            return Note.SecondsToTicksFromDouble(seconds);
        }

        // Token: 0x06000E3B RID: 3643 RVA: 0x0004C7FF File Offset: 0x0004A9FF
        public int CompareTo(TrackTick other)
        {
            return this.value.CompareTo(other.value);
        }

        // Token: 0x06000E3C RID: 3644 RVA: 0x0004C812 File Offset: 0x0004AA12
        public bool Equals(TrackTick other)
        {
            return this.value.Equals(other.value);
        }

        // Token: 0x06000E3D RID: 3645 RVA: 0x0004C825 File Offset: 0x0004AA25

        // Token: 0x06000E40 RID: 3648 RVA: 0x0004C868 File Offset: 0x0004AA68


        // Token: 0x06000E41 RID: 3649 RVA: 0x0004C8C4 File Offset: 0x0004AAC4
        public float LinearMapUnclamped(TrackTick fromMin, TrackTick fromMax)
        {
            if (fromMax == fromMin)
            {
                return (float)((this.value <= fromMin) ? 0 : 1);
            }
            return (float)(this.value - fromMin) / (float)(fromMax - fromMin);
        }

        // Token: 0x06000E42 RID: 3650 RVA: 0x0004C918 File Offset: 0x0004AB18

        // Token: 0x06000E43 RID: 3651 RVA: 0x0004C92C File Offset: 0x0004AB2C


        // Token: 0x06000E44 RID: 3652 RVA: 0x0004C93E File Offset: 0x0004AB3E
        

        // Token: 0x06000E48 RID: 3656 RVA: 0x0004C9B4 File Offset: 0x0004ABB4
        public static TrackTick LerpWithFloat(TrackTick a, TrackTick b, float t)
        {
            return a + (long)((float)(b - a) * t);
        }

        // Token: 0x04000EB0 RID: 3760
        public static readonly TrackTick Zero = default(TrackTick);

        // Token: 0x04000EB1 RID: 3761
        public static readonly TrackTick OneSecond = 100000L;

        // Token: 0x04000EB2 RID: 3762
        public static readonly TrackTick OneSemisecond = 1000L;

        // Token: 0x04000EB3 RID: 3763
        private long value;
    }
}
