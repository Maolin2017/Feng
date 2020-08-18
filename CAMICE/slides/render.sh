clean(){
sed -e 's/\(^\|[^*]\)\(\t\|* \|1\. \)//g' $1
}

main()
{
local SELF=${BASH_SOURCE[0]}
SELF=`readlink -f $SELF`
local DIR=`dirname $SELF`
echo $SELF
IN=${1:-MandM_BrachyCompMethod.md}
ALI=${IN%.*}
#OPT=" --filter pandoc-mustache --filter pandoc-citeproc"
OPT=" --filter pandoc-mustache --filter pandoc-citeproc \
--toc -c ../pandoc.css -s"
#cat $ALI.md | 
clean $ALI.md | pandoc $OPT -f markdown -o $ALI.direct.docx

clean $ALI.md | pandoc $OPT --webtex -f markdown+smart -t html | tee $ALI.html \
| pandoc -f html -o $ALI.docx



}
main "$@"
