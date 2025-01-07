set -x
cd submissions/project2 || exit
find . -maxdepth 1 -type d ! -name '.' | while read dir; do
    echo '${dir}'
    cd $dir
    tar -xvf tar.tar
    find . -maxdepth 1 ! -name 'lib_tar.c' -type f -exec rm -f {} +    
    rm -r archive
    cd ..
done
tar -cvf all_sub.tar.gz *
