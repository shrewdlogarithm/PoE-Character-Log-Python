<html>
    <head>
        <title>POE Tracked Characters</title>
        <script>
            function clipto() {
                document.execCommand("selectall",null,false);
                document.execCommand('copy');
            }
        </script>
        <link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/poe.css">
    </head>
    <body>
    <h2>POEClog</h2>
    <h3>Questions/Issues/Ideas - check our Github at <a href="https://github.com/shrewdlogarithm/PoE-Character-Log-Python">https://github.com/shrewdlogarithm/PoE-Character-Log-Python</a></h3>
    <P>
        <table>
        %   for account in sorted(accounts, key=str.casefold):
        %       first = True
        %       for ch in accounts[account]:
        %           char = accounts[account][ch]
        %           if "clogextradata" in char and int(char["level"]) > 10:
        %               league = char["clogextradata"]["league"]
        %               if len(league) > 15: 
        %                   league = league[0:12] + "..."
        %               end
        %               if first:
        %                   first = False
                            <tr><td>&nbsp;</td></tr>
                            <tr><td colspan=3><a href="https://www.pathofexile.com/account/view-profile/{{account}}/characters"><h3>{{account}}</h3></a></td><td>Level</td><td>Build</td><td colspan=2>Path of Building</td><td>Skills</td></tr>
        %               end
                        <tr>
                            <td>{{char["name"]}}</td>
                            <td>{{char["class"]}}</td>
                            <td>{{league}}</td>
                            <td>{{char["clogextradata"]["levelfrom"]}}-{{char["level"]}}</td>
                            <td><a href={{f'logs/{account}-{ch}.html'}}>Build Log</a></td>
                            <td><input type="text" size=10 value='{{char["clogextradata"]["pcode"]}}' onClick="clipto()"/></td>
                            <td><a href={{f'pob/builds/{account}-{ch}.xml'}}>XML</a></td>
                            <td>{{char["clogextradata"]["skillset"]}}</td>
                        </tr>
        %           end
        %       end
        %   end
        </table>
    <h3>Questions/Issues/Ideas - check our Github at <a href="https://github.com/shrewdlogarithm/PoE-Character-Log-Python">https://github.com/shrewdlogarithm/PoE-Character-Log-Python</a></h3>
    </body>
</html>