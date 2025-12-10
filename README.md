# lokaverkefni.banki

Við gerðum verkefni sem er teingt bánka, bánkin okkar virkar þannig að þegar við setjum airtag við censor þa birtast blátt ljós á ljósaperuni og hurðin opnast, en ef censorin lés ranga airtag þá kemur rautt ljós.

Við notuðum tvo ESP32 og einn Rasberry py4, þau virka þannig að ESP sem er með boxinu er teingdur við ljósaperuna og mótorinn sem opnar og lokar hurðina, hinn ESP er teingdur censornum og skjá. Síðan er Rasberry py sem tekur tildæmis á moti því sem ESP 1 er að senda og sendir því síðan strax á ESP 2 sem sagt Rasberry py er þá millipunktin a milli þeirra.

Það sem klikkaði var að við gleimdum að designa festingu fyrir mótor og út af því virkaði ekki mótorinn og náðum ekki að teingja við rasberry py. annars allt hit virkaði.
