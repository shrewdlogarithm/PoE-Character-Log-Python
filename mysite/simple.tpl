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
        <tr><td></td><td>Level</td><td>API Data</td><td colspan=2>Logs</td><td colspan=2>Path of Building</td></tr>
        % from getchars import getchars
        % accounts = getchars()
        % for account in accounts:
            <tr><td><h3>Account {{account}}</h3></td></tr>
            % for char in accounts[account]:
                <tr>
                    <td>{{char["charname"]}} - {{char["classname"]}} - {{char["league"]}}</td>
                    <td>{{char["levelfrom"]}}-{{char["levelto"]}}</td>
                    <td><a href={{char["datapath"]}}>JSON</a></td>
                    <td><a href={{char["logpath"]}}>Txt</a></td>
                    <td><a href={{char["htmlpath"]}}>Web</a></td>
                    <td><input type="text" size=10 value='{{char["pcode"]}}' onClick="clipto()"/></td>
                    <td><a href={{char["filepath"]}}>XML</a></td>
                </tr>
    </body>
</html>