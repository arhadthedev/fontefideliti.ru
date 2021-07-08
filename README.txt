NAME

       build_site.py - generate <https://fontefideliti.ru> from resources

SYNOPSIS

       python src/build_site.py [-h | --help] <res_dir>

DESCRIPTION

       Take a file database from RES_DIR directory and populate
       a current directory with a static site file structure.

OPTIONS

       -h
       --help
       Show a help message and exit.

       <res_dir>
       Path to a file database with source data and resources.

NOTES

       If an output directory is not empty, the script overwrites document files
       and skips already presented image variants. So if you change an original
       image, delete all of its variants from an output directory to force their
       regeneration.

       To run the script, Python 3.3 or above is required.

AUTHOR

       Written by Oleg Yarigin <oleg@arhadthedev.net>.

REPORTING BUGS

       Report any bugs to
       <https://github.com/arhadthedev/fontefideliti.ru/issues>

COPYRIGHT

       Code: Copyright © 2015–2021 Oleg Yarygin.  License MIT:
       <https://opensource.org/licenses/MIT>.  This is free software:
       you are free to change and redistribute it. There is NO WARRANTY,
       to the extent permitted by law.

       Resources: Copyright © 2015–2021 Oleg Yarygin, Natalya Yarigina.
       License CC BY-SA 4.0:
       <https://creativecommons.org/licenses/by-sa/4.0/legalcode>.

       This project uses baguetteBox.js by Marek Grzybek
       <https://github.com/feimosi/baguetteBox.js>. Copyright (c) 2018
       feimosi. License MIT.
