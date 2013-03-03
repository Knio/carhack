
all: \
	assets

assets: \
	web/assets/normalize.css \
	web/assets/plok.css \
	web/assets/plok.js \
	web/assets/pyy.js \
	web/assets/moment.min.js \
	web/assets/fonts/boeCNmOCCh-EWFLSfVffDg.woff \
	web/assets/fonts/KT3KS9Aol4WfR6Vas8kNcg.woff \
	web/assets/fonts/9k-RPmcnxYEPm8CNFsH2gg.woff \
	web/assets/fonts/wkfQbvfT_02e2IWO3yYueQ.woff \

web/assets/normalize.css:
	wget -O $@ http://necolas.github.com/normalize.css/2.1.0/normalize.css

web/assets/plok.css:
	wget -O $@ http://plok.zkpq.ca/plok.css

web/assets/plok.js:
	wget -O $@ http://plok.zkpq.ca/plok.js

web/assets/pyy.js:
	wget -O $@ http://pyy.zkpq.ca/pyy.js

web/assets/moment.min.js:
	wget -O $@ https://raw.github.com/timrwood/moment/2.0.0/min/moment.min.js

web/assets/fonts/boeCNmOCCh-EWFLSfVffDg.woff:
	wget -O $@ http://themes.googleusercontent.com/static/fonts/lato/v6/boeCNmOCCh-EWFLSfVffDg.woff

web/assets/fonts/KT3KS9Aol4WfR6Vas8kNcg.woff:
	wget -O $@ http://themes.googleusercontent.com/static/fonts/lato/v6/KT3KS9Aol4WfR6Vas8kNcg.woff

web/assets/fonts/9k-RPmcnxYEPm8CNFsH2gg.woff:
	wget -O $@ http://themes.googleusercontent.com/static/fonts/lato/v6/9k-RPmcnxYEPm8CNFsH2gg.woff

web/assets/fonts/wkfQbvfT_02e2IWO3yYueQ.woff:
	wget -O $@ http://themes.googleusercontent.com/static/fonts/lato/v6/wkfQbvfT_02e2IWO3yYueQ.woff


clean:
	-rm web/assets/*
