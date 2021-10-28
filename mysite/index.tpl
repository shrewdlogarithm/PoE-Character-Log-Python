% import os,json
% if os.path.exists("accountdb.json"):
%   with open("accountdb.json") as json_file:
%     accounts = json.load(json_file)

<html>
    <head>
        <title>PoEClog</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script>
            function clipto() {
                var oldc = $(this).val()
                $(this).val($(this).data("pcode"))
                document.execCommand("selectall",null,false);
                document.execCommand('copy');
                $(this).val("Pastecode Copied")
                setTimeout($.proxy(function() {
                    $(this).val(oldc)
                },this), 2000);
                
            }
        </script>
        <link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/poe.css">
    </head>
    <body>
    <h2>PoEClog</h2>
    <h3>Questions/Issues/Ideas - <a href="https://github.com/shrewdlogarithm/PoE-Character-Log-Python">click here</a></h3>
    <P>
        <table>
        %   for account in sorted(accounts, key=str.casefold):
        %       first = True
        %       for ch in accounts[account]:
        %           char = accounts[account][ch]
        %           if "clogextradata" in char and int(char["level"]) > 10:
        %               league = char["league"]
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
                            <td><input type="text" readonly size=13 value='Click for Pastecode' onClick="clipto.call(this)" data-pcode='{{char["clogextradata"]["pcode"]}}'/></td>
                            <td><a href={{f'pob/builds/{account}-{ch}.xml'}}>XML</a></td>
                            <td>{{char["clogextradata"]["skillset"]}}</td>
                        </tr>
        %           end
        %       end
        %   end
        </table>
    <h3>Questions/Issues/Ideas - <a href="https://github.com/shrewdlogarithm/PoE-Character-Log-Python">click here</a></h3>
    </body>
</html>