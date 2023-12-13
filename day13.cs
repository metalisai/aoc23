using var file = new StreamReader("input13");
var data = file.ReadToEnd();

var maps = data.Split("\n\n").Where(x => !string.IsNullOrEmpty(x)).ToArray();
string[][] mapsL = maps.Select(x => x.Split("\n").Where(x => !string.IsNullOrEmpty(x)).ToArray()).ToArray();
char[][][] mapsC = mapsL.Select(x => x.Select(y => y.ToCharArray()).ToArray()).ToArray();

int getScore(char[][][] maps, bool part1) {
    int sum = 0;
    foreach (var map in maps) {
        Func<List<(int location, bool vertical)>> findMatch = () => {
            List<(int, bool)> reflectionsH = FindReflectionsH(map).Select(x => (x, false)).ToList();
            List<(int, bool)> reflectionsV = FindReflectionsH(TransposeMap(map)).Select(x => (x, true)).ToList();
            var matches = reflectionsH.Concat(reflectionsV).ToList();
            return matches;
        };
        var originalMatch = findMatch()[0];
        var scoreMatch = originalMatch;

        Action<int, int> flip = (int i, int j) => {
            if (map[i][j] == '.') {
                map[i][j] = '#';
            } else if (map[i][j] == '#') {
                map[i][j] = '.';
            }
        };
        if (!part1) {
            for( int i = 0; i < map.Length; i++) {
                for (int j = 0; j < map[0].Length; j++) {
                    flip(i, j);
                    var matches = findMatch();
                    foreach (var match in matches) {
                        if (match != originalMatch) {
                            scoreMatch = match;
                            flip(i, j);
                            goto end;
                        }
                    }
                    flip(i, j);
                }
            }
        }
end:
        if (!scoreMatch.vertical) {
            sum += (scoreMatch.location+1) * 100;
        } else {
            sum += scoreMatch.location+1;
        }
    }
    return sum;
}

int part1S = getScore(mapsC, true);
Console.WriteLine($"Part1: {part1S}");
int part2S = getScore(mapsC, false);
Console.WriteLine($"Part2: {part2S}");

char[][] TransposeMap(char[][] map) {
    char[][] result = new char[map[0].Length][];
    for (int i = 0; i < map[0].Length; i++) {
        result[i] = new char[map.Length];
        for (int j = 0; j < map.Length; j++) {
            result[i][j] = map[j][i];
        }
    }
    return result;
}


bool IsMatch(int idx, char[][] map) {
    if (idx == 0) {
        return true;
    }
    int rowsLeft = Math.Min(idx, map.Length - idx - 2)+1;
    for (int i = 1; i < rowsLeft; i++) {
        var first = new string(map[idx-i]);
        var second = new string(map[idx+1+i]);
        if (first != second) {
            return false;
        }
    }
    return true;
}

List<int> FindReflectionsH(char[][] map) {
    List<int> candidates = new();
    for (int row = 1; row < map.Length; row++) {
        var line = new string(map[row]);
        var prevLine = new string(map[row - 1]);
        if (line == prevLine) {
            candidates.Add(row-1);
        }
    }
    List<int> matches = new();
    foreach (var candidate in candidates) {
        if (IsMatch(candidate, map)) {
            matches.Add(candidate);
        }
    }
    return matches;
}
