import cherrypy
import random

class Sentimento:
    def index(self):
        return """
        <html>
	<head>
		<style>
		body
		{
			background-color:white
			text-color
		}

		div {
			background-color: White
			float: left
			width: 20%
			height: 230px
			border-width:1px
			border-style:solid
			border-color:#000000
		}
		input.go
		{
			height: 50px
			width: 100px
		}

		</style>
		<title>SentimentAnalysisScraperSomething-Tool - By Jannik, Stefan and Lars</title>
	</head>
	<body>
		<form action="analyze">>
			<div>
				<h1>Step 1</h1>
				<p>Enter a topic: <input type="text" name="Topic"> </p>
			</div>
			<div>
				<h1>Step 2</h1>
				<p>Select which sites to search:</p>
				<input type="checkbox" name="INF"> information.dk <br>
				<input type="checkbox" name="TV2"> nyhederne.tv2.dk <br>
				<input type="checkbox" name="POL"> politiken.dk<br>
				<input type="checkbox" name="EB"> ekstrabladet.dk<br>
				<input type="checkbox" name="BT"> bt.dk<br>
			</div>
			<div>
				<h1>Step 3</h1>
				<p> [ COMING SOON! ] </p>
			</div>
			<div>
				<h1>Step 4</h1>
				<p><input type="submit" value="Submit" class="go"></p>
			</div>
		</form>
	</body>
</html>
        """
    index.exposed = True

    def getscore(self):
        return random.uniform(4.5, 7.0)
    getscore.exposed = True

    def analyze(self, Topic=None, INF=0, TV2=0, POL=0, EB=0, BT=0):
        results = """<html>
        <head>
        <title>""" + Topic  +  """</title>
        </head>
        <body>
        <h1>""" + Topic + """</h1>"""

        total = 0
        count = 0

        if(INF):
            count = count + 1
            score = self.getscore()
            total = total + score
            results += """<h1>information.dk</h1>
            <p>Result: %.2f </p>""" % score
        
        if(TV2):
            count = count + 1
            score = self.getscore()
            total = total + score
            results += """<h1>information.dk</h1>
            <p>Result: %.2f </p>""" % score

        if(POL):
            count = count + 1
            score = self.getscore()
            total = total + score
            results += """<h1>information.dk</h1>
            <p>Result: %.2f </p>""" % score

        if(EB):
            count = count + 1
            score = self.getscore()
            total = total + score
            results += """<h1>information.dk</h1>
            <p>Result: %.2f </p>""" % score

        if(BT):
            count = count + 1
            score = self.getscore()
            total = total + score
            results += """<h1>information.dk</h1>
            <p>Result: %.2f </p>""" % score

        avg = total / count
        results += """<br></br><br></br><h3>Average</h3>
        avg = %.2f""" % avg

        results +=  """</body>
        </html>
        """
        return results
    analyze.exposed = True

cherrypy.quickstart(Sentimento())