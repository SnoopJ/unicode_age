# Generated file, do not edit
import zlib
import base64

UCD_VERSION = (18, 0, 0)

version_map = [(1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (5, 0), (5, 1), (5, 2), (6, 0), (6, 1), (6, 2), (6, 3), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (12, 1), (13, 0), (14, 0), (15, 0), (15, 1), (16, 0), (17, 0), (18, 0)]

def iter_spans():
    start = 0
    for count, packed_ver in zip(_counts, _versions):
        stop = start + ord(count)
        if packed_ver:
            yield (start, stop, *version_map[packed_ver-1])
        start = stop + 1

_versions = zlib.decompress(base64.a85decode(rb'''
GhSupfokDE$ksb!0ZO[UYi%G=s52TGPj@PtLj@WD,<uMXFAO9ZOGf8oY<j]^4'@e[C4mb8MEkXdJB&
9C1PG2$Oc'n]"%n4^l`qGpGi'e[+Ks^;dM%j>q>r_b;EbpLPS([2(63MfmDQ+Ka"'a:P_O?b.9Wt;J
=UGUFB0K2Lik4*D:&TH/Past)&MY>f-'8ZW`+=Am@HiT7H-h)a-G+hkBC=7<ttB>/rPb'<uDo!k^M6
ghiE@:.)8c6"j<rl/k<d,]@(N(QdFcsN`JGI%+^()+NDMu\D7R'gd[dc,#?EpW5,fj+J@QeZH.[j!U
q"i31(h[1eC&uRj=%3:gg(gj@PdV/8jGJZ"TiEYRIL^f@g"[^,Yu28+4e]a[hPq[,;-ll;FT6F@.NK
UK+BBR"0Q]!K7uO63@nO],RHnG.!6/,h6'oj,HQt)2,tF-RDBVXPZB7-E\]^F`S=4%*&_O$W%LA8rI
!ar>#ct9=mhj^Z;,kq^9<&#=E6W?K1V?JJAeC14'^&=0\Kg[U$t<eLl_\(82Kr5\NZE=>nIAoc8Tns
+D+l=+./O^>37Q;M4i`)^r'+;TN9B0kFX5AQ<EtH?bBYVt%SPR_H[Q^j6iaEiF0:nbZe5fiI*6!Elo
+6B\KbF4/[W`FBWDNHHQH70@'tK%7h''oq;E!*KHB+Yk3e`/b@OdJ8<29*%N6>g?@fk63)6/\sND$c
9M"N/4<i#s'+^%qGl\^s)OcAK\pQb=.Q4VCjt;^Mr1O7-.Wl?#?<n-<crPOh*dZk&G@[qXUb<5lMCR
rdYK_Z-[>hTK16'cd^F1rB.-K"]<:t!D*,!S:`t:f=U<sh*>4)EJ6KI^EK?!A,_Es\qqGBSphTA^)<
2d@i1M(a4Z7VkA'1rM\W>;?E=iW"iCir^6jtTi4U1DDT>T,dB*fKN\n?BA=Pkn/+<f7mM6c4)u3`Ym
`?g9!4E%.6D)=>47.;hpdkd6+E*"g&*tB/DeQq?ra;6`jU*6`E8c^WX(79=YU*uN'tMZFSe#*Jqp@N
C476&dhlUb:`j<%QT63;km<6GC^j0T0XEr@7=6QCG(7o6SbT,rFM)XB`O4M8):T0\1!.M'5Q0&Z-BY
4h`id//uk]RBa:64h]eo@U#O%\m[''220rYN(>ODA89)i@A8IY5u.D8r_H7i:p6&j&!@(EN_8CY/l`
aTaa),9E=7>&a143O/At,^6U?,^9YK\R)Ni__6AYf[Gs+hm_OS90%Qo8hN-caKI$*1H5#/3KVU\-[q
sg/0+F[O<3Z;B1S3.lZi8F0!Y^B6dpuAg")oY]P'9l^(A_ld(p#Dr<NnEU?OnnW*)R
'''))

_counts = zlib.decompress(base64.a85decode(rb'''
GhS-XgM\'U'gCf)S_qZ:XOh6k0=u#?[F^GB8aJES;A'caPGhJ9&@Z@'!`CKh80<qlKFffdKLF0"Pp-
BgZrLdRX/\!jTf"S9`R:oY1gEYl$P,AXXi(=SPWs`fbdqP6A*qt&R5o?6GAc:u[l/?a'9uOe5%8bsK
'?Hqa;`)td*,1@838"Fdkj'ogAR8'N2D7lMdnCpl[p`1Wj69G79sHte0)CZ%V\%u/h.!]8?j2bA7A8
DLa(;F2dj4^ZBXnd2O%(0K;"OpC62H/[%GbkXCaJFG,!Ut&VL-F[S/m'O<5b+4NJhrao-GkK*!&q\/
,uQBtW\LKmSL1L3n_<hH8TrO\<N)E30g7!-B)U;"?elF^tmcr'kc`Hj0&dhI-YmC\TK)%(*j4@ZJP7
-4?AJM+(IlY<4KV\VE[o2=X0.i2BJ&("%tqDAT+e2E5]Fmh"Ja)7(h+n20r?Ue%4a6i]m8&.tt58<d
'qP!SI('Jea#;'h!?D6.6.3haYmF:q]+04G48!K)V-clREkR(qH%8ekeZhJ"#MOZ\_(g(#ZLDWGLLQ
f+l"k!&A_lf]0WW*K<bSpq:,EQ>n5Kg*%':>IU+<<IE((cf@E&_5AI]dl>tU.SB[J;lPa$GjD`1CEh
4\OeP,Tn\*]7$F'M'2PnTYXfiH=.,+HNFPMWS8k!;@^64=IYMQ/-$I,j-'bJ*Ls6Van*e\fqSuCDC8
UTA1p<'+@s`d(J]$q7`=O+Z$rXM6X8m)I:0=<KSB8C!#K_3*,7KNYF<[dF&mWqNh2Uo7;RQBEMo\(#
-*:OP7,K/f06!FXN05/jeJn6>T.3e28m(c#/4"]?'+R2qP):Yh*N0nqqOg5tQ0tA/q'^]Y%O((N?J3
7s?#4B6g.JJ'HET)9J;8tN<.`igf,:7-;#uBR/Y>Oac/^<YPk:c-\E)hu^YqB$h%Uuf.ZRY5#O%;GF
_)[](raZshul5:AjSUD9>s)+MIhgHM#<2YPbG8kA;QnQDsMHmK_DGc@JQO^?Kq-SU)m60J,QW%_7;s
#(@BlU<I's)^5C&pm46o[H0O*P)H5q=Z9b6W"WJoh<4WgtRjJm:P!;]*Z,lsEQtknPMP]eP74AJ7et
;7aPopu]mc$E,!WH/5;-+jqpgm@Nqt31^g94fF,Ds7`E!b=e(E1K=j7+<.hg;-.b_la_Zsb[kXW7(+
@s4'%/5YpNJ=Yf..^oI'J/qGpi][>[cjHZqh_e$PW9A]mguGruk'Bbhc`2;IFJK,cPc5=Ul?'>JNE&
4_eY@H-0>o,8-mZ0H<X[%CDkl1Iq^bHnC7!=0?u_DXK?^-#52$7*P'R95VLc`"S1X:_Wm:s'%"cK@6
nWMt_o(LqM&'*N#E:AsS[d46LZT!9c;+.B)li&2oumuK+Rhg.c_qX26#+84p'rpZj\#0<Y1j6B!Z]b
ZJiuXRk\`LD$"KV`.`Wj(,'>a2J&%-4&JP/1>%LqEZO3ZLPd<,baI0%oS[0*nSnht"h8o7&4u?VLjA
L9aGT:OnHO9$RC`1dFR4c)5juncR3?d?`E&Q7CLn_-5H'[L,'7PK_A.$;f?(a')H6`s85=9.`WF6oA
:C<t5.637s",lc<&2'KBegR9DomYL]HW??^-p(7u5Mqj(YFeI<12^A_@Wl)WiOQg\2^k\[S_md3[kG
-rh`Ui2MskSq+UX[Q!#DWA%4`U;q]=47o?G1TMiX<Um[lZQ@\/K_f<Q6SfgP4CD]%g?pmYJ@R8Jifq
5`C&I.1r5hqi`eG:))<o,?h.Lg>m"2kSrPq8.FL<TF5YSTg]ArD'>]DqbUJYIY)1^Ci\L:MV261H"'
M\S!3.3*K)"ahput2(u)ZkOS_4k)aR-Cdn*\K?mC0=%F%JqRpO(P3j'R&,bDN$q#HNp6V,#XF3'NMt
;t?3)?M6\qe![UX4IY\$q+'%NE"Pb[g%^Pc!To&G;d!Y.<=Q7]dbOEUWk%+o8+/h"STs>3d)ZTC^P;
b'DZ`:-u'VT.VYi:R4i@>TciZW52<^!cMG;erM-@3[*C^2oMe.m)8]]kY!-q8L6n&&;4m-=>LG\KF/
q9qU':tRm5eo@!c$"/gk.2+AC5F]M,itL<TCeXI\T+@8D3j?mmQ%"JZ,I_3JD"fXDJS>Dq,cW-hTQo
`US6244Z9@3EW;'\\5DZ\0ig`k`.I-'0B"_A$-=`f,/E9u4hcZ(Y:!D,QYu;qe-'V.BB5)5+4iTVm/
KW>pq7"*r+<#9NRbe,1X8)@Q2rp\E^mrQOeNqoO%=g"$O!mAoOZ\)2H]]7#+jeJI+miG[>XIJG>@?G
G(*n=tKh\G4HU>9CN$+)h+-#DV$c^=R]&j3>dIq8JQ`rrjnd"R?    ''')).decode("utf-8")

