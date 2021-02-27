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
        <table>
        <tr><td></td><td>Level</td><td colspan=2>BuildLog</td><td>Path of Building</td><td>Skills</td></tr>
        % import os,json
        % accountdb = "data/accountdb.json"
        % accounts = {}
        % if os.path.exists(accountdb):
        %   with open(accountdb) as json_file:
        %       accounts = json.load(json_file)
        %       for account in accounts:
                    <tr><td><h3>Account {{account}}</h3></td></tr>
                    % for ch in accounts[account]:
                    %   char = accounts[account][ch]
                    %   if "levelfrom" in char and int(char["level"]) > 10:
                            <tr>
                                <td>{{char["name"]}} - {{char["class"]}} [{{char["league"]}}]</td>
                                <td>{{char["levelfrom"]}}-{{char["level"]}}</td>
                                <td><a href={{f'logs/{account}-{ch}.log'}}>Txt</a></td>
                                <td><a href={{f'logs/{account}-{ch}.html'}}>Web</a></td>
                                <td><input type="text" size=10 value='{{char["pcode"]}}' onClick="clipto()"/></td>
                                <td>{{char["skillset"]}}</td>
                            </tr>
    </body>
</html>