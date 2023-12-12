using var fs = new FileStream("input12", FileMode.OpenOrCreate);
using var sr = new StreamReader(fs);

long total = 0;

List<(string, int[])> lines = new ();

while (sr.Peek() >= 0)
{
    var line = sr.ReadLine();
    var conds = line?.Split(' ')[0] ?? "";
    var counts = line?.Split(' ')[1].Split(',').Select(x => int.Parse(x)).ToArray() ?? Array.Empty<int>();
    if (true) {
        conds = string.Join('?', Enumerable.Range(0, 5).Select(_ => conds));
        counts = Enumerable.Repeat(counts, 5).SelectMany(x => x).ToArray();
    }
    lines.Add((conds, counts));
}

var sw = new System.Diagnostics.Stopwatch();
sw.Start(); 

object locker = new object();
int linesSolved = 0;

Parallel.ForEach(lines.Chunk(100), (chunk) => {
    foreach (var line in chunk) {
        var (conds, counts) = line;
        long cur = findValidPermutations(conds, counts);
        Interlocked.Add(ref total, cur);
        Interlocked.Increment(ref linesSolved);
        lock (locker) {
            Console.WriteLine($"{linesSolved:D4}/{lines.Count} solved"); 
            Console.SetCursorPosition(0, Console.CursorTop - 1);
        }
    }
});

sw.Stop();

Console.WriteLine("\n");
Console.WriteLine("total: " + total);
Console.WriteLine("time: " + sw.ElapsedMilliseconds);

// IMPLEMENTATION:

string getKey(char[] conditions, int[] counts, int idx, int run) {
    return string.Join(',', counts)+"|"+new string(conditions[idx..])+"|"+run;
}

long recurse(char[] conditions, int[] counts, int idx, int run, Dictionary<string, long> cache) {
    var key = getKey(conditions, counts, idx, run);
    if (cache.ContainsKey(key)) {
        return cache[key];
    }
    while (true) {
        if (idx == conditions.Length) {
            if (counts.Length == 0 || (counts.Length == 1 && run == counts[0])) {
                return 1;
            }
            return 0;
        }
        else if (conditions[idx] == '#') {
            if (counts.Length == 0 || run+1 > counts[0]) {
                return 0;
            }
            idx += 1;
            run += 1;
            continue;
        }
        else if (conditions[idx] == '.') {
            if (run > 0 && (counts.Length == 0 || run < counts[0])) {
                return 0;
            }
            if (run > 0) {
                counts = counts[1..];
                idx += 1;
                run = 0;
                continue;
            } else {
                idx += 1;
                continue;
            }
        }
        else if (conditions[idx] == '?') {
            break;
        } else {
            throw new Exception("Invalid condition");
        }
    }
    var sb = conditions.ToArray();
    sb[idx] = '.';
    long res = recurse(sb, counts, idx, run, cache);

    sb = conditions.ToArray();
    sb[idx] = '#';
    res += recurse(sb, counts, idx, run, cache);

    cache[key] = res;
    return res;
}

long findValidPermutations(string conditions, int[] counts) {
    var condsChar = conditions.ToCharArray();
    Dictionary<string, long> cache = new ();
    long validCount = recurse(condsChar, counts, 0, 0, cache);
    return validCount;
}
