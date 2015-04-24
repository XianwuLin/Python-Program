vim个人配置
===========
鉴于现在vim配置较为复杂，而且与多个软件有联系，现把主要的操作写下来便于查看：

快捷键
------
**功能键**

1.  F1		保存
6.  F2		建立Tags
2.  F4		格式化代码
7.  F5		编译C/C++程序
8.  C-F5	GDB调试C/C++程序
9.  F6		运行C/C++程序
3.  F9	 	执行Python
4.  F10		执行R语言
5.  F11		编译Latex代码
6.  F12		调用Chrome查看markdown

**其他键**

1.  ,tl		打开（关闭）函数列表
2.  :A		.cpp/.h转换(:AS :AV则同时打开到窗口)
3.  Tab		部分代码补全
4.  ,nt		打开文件浏览窗口
4.  C-n		补全Python代码 

在VIM原生基础上现在拥有的功能
----------------------------------
1. 自动补全

	>C++:	 	ctags、cscope、omni、taglist
	>
	>Python:	python_pydiction
	z
	>通用:		snipMate

2. 较好的格式化代码能力	autoformat
3. markdown高亮		mkd

附上我的vim配置文件
-------------------
注：环境：win7 64bit，版本：vim 7.3，主要面向gvim（vim的GUI版本）
	
	set nocompatible
	filetype plugin on
	source $VIMRUNTIME/vimrc_example.vim
	source $VIMRUNTIME/mswin.vim
	if(has("win32") || has("win95") || has("win64") || has("win16"))
		let g:vimrc_iswindows=1
	else
		let g:vimrc_iswindows=0
	endif
	autocmd BufEnter * lcd %:p:h
	"设置界面
	set guioptions-=T
	behave mswin
	set guifont=楷体:h14
	set mouse=a
	set nofoldenable
	set nocp
	colorscheme breeze
	set display=lastline
	"设置文字
	set fileencodings=utf-8,chinese,latin-1
	set fileencoding=utf-8
	set nobackup
	set iskeyword+=_,$,@,%,#,-
	set wrap
	"set linebreak
	set display=lastline
	let vimrplugin_i386 = 1
	let vimrplugin_r_path = "D:\\program files\\R\\R-2.15.2\\bin\\x64"
	let g:pydiction_location='D:\program files\Vim\vimfiles\plugin\complete-dict'
	let Tlist_Use_Right_Window = 1
	let Tlist_Show_One_File=1
	let Tlist_Exit_OnlyWindow=1
	set vb t_vb=
	set nu!
	set helplang=cn
	set cindent
	set autoindent
	set tags=tags
	set tags+="D:/program files/Vim/vimfiles/epp_src/cpp"
	set autochdir
	set tabstop=8
	set backspace=2
	
	"绑定按键
	map <F1> :w!<CR>
	map <F9> <F1>:!python "%"<CR>
	map <F4> :Autoformat<CR><CR>
	map <F10> <F1><Plug>RSendFile
	map <F11> :Tex<CR>
	map <F12> <F1>:silent !start C:\Program Files (x86)\Google\Chrome\Application\chrome.exe "%:p"<CR>
	map ,tl :TlistToggle<CR>
	map ,nt ::NERDTree<CR><CR>
	
	""用Vim编译C/C++
	if &filetype == 'c' || &filetype == 'cpp'
		set encoding=cp936
		set fileencoding=cp936
	endif	
	"定义CompileRun函数，用来调用进行编译和运行
	map <F5> :call CompileRun()<CR>
	map <F6> :call Run()<CR>
	map <C-F5> :call Debug()<CR>
	func CompileRun()
		exec "w"
		if &filetype == 'c'
			exec "!gcc -Wall % -g -o %<.exe"
		elseif &filetype == 'cpp'
			exec "!g++ -Wall % -g -o %<.exe"
		endif
	endfunc
	"定义Run函数
	func Run()
		if &filetype == 'c' || &filetype == 'cpp'
			exec "!%<.exe"
		endif
	endfunc
	"定义Debug函数，用来调试程序
	func Debug()
		exec "w"
		"C程序
		if &filetype == 'c'
			exec "!gcc % -g -o %<.exe"
			exec "!gdb %<.exe"
		elseif &filetype == 'cpp'
			exec "!g++ % -g -o %<.exe"
			exec "!gdb %<.exe"
		endif
	endfunc
	
	set diffexpr=MyDiff()
	function MyDiff()
		let opt = '-a --binary '
		if &diffopt =~ 'icase' | let opt = opt . '-i ' | endif
		if &diffopt =~ 'iwhite' | let opt = opt . '-b ' | endif
		let arg1 = v:fname_in
		if arg1 =~ ' ' | let arg1 = '"' . arg1 . '"' | endif
		let arg2 = v:fname_new
		if arg2 =~ ' ' | let arg2 = '"' . arg2 . '"' | endif
		let arg3 = v:fname_out
		if arg3 =~ ' ' | let arg3 = '"' . arg3 . '"' | endif
		let eq = ''
		if $VIMRUNTIME =~ ' '
			if &sh =~ '\<cmd'
				let cmd = '""' . $VIMRUNTIME . '\diff"'
				let eq = '"'
			else
				let cmd = substitute($VIMRUNTIME, ' ', '" ', '') . '\diff"'
			endif
		else
			let cmd = $VIMRUNTIME . '\diff'
		endif
		silent execute '!' . cmd . ' ' . opt . arg1 . ' ' . arg2 . ' > ' . arg3 . eq
	endfunction
	
	""调用latex进行编译
	command! Tex call Tex()
	function! Tex()
		w
		!latex %
		silent !latex %
		silent ! dvipdfmx %:r
		silent ! start %:r.pdf
	endfunction
	
	""vim自动补全
	map <F2> :call Do_CsTag()<CR>
	nmap <C-@>s :cs find s <C-R>=expand("<cword>")<CR><CR>:copen<CR>
	nmap <C-@>g :cs find g <C-R>=expand("<cword>")<CR><CR>
	nmap <C-@>c :cs find c <C-R>=expand("<cword>")<CR><CR>:copen<CR>
	nmap <C-@>t :cs find t <C-R>=expand("<cword>")<CR><CR>:copen<CR>
	nmap <C-@>e :cs find e <C-R>=expand("<cword>")<CR><CR>:copen<CR>
	nmap <C-@>f :cs find f <C-R>=expand("<cfile>")<CR><CR>:copen<CR>
	nmap <C-@>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>:copen<CR>
	nmap <C-@>d :cs find d <C-R>=expand("<cword>")<CR><CR>:copen<CR>
	function Do_CsTag()
		let dir = getcwd()
		if filereadable("tags")
			if(g:iswindows==1)
				let tagsdeleted=delete(dir."\\"."tags")
			else
				let tagsdeleted=delete("./"."tags")
			endif
			if(tagsdeleted!=0)
				echohl WarningMsg | echo "Fail to do tags! I cannot delete the tags" | echohl None
				return
			endif
		endif
		if has("cscope")
			silent! execute "cs kill -1"
		endif
		if filereadable("cscope.files")
			if(g:iswindows==1)
				let csfilesdeleted=delete(dir."\\"."cscope.files")
			else
				let csfilesdeleted=delete("./"."cscope.files")
			endif
			if(csfilesdeleted!=0)
				echohl WarningMsg | echo "Fail to do cscope! I cannot delete the cscope.files" | echohl None
				return
			endif
		endif
		if filereadable("cscope.out")
			if(g:iswindows==1)
				let csoutdeleted=delete(dir."\\"."cscope.out")
			else
				let csoutdeleted=delete("./"."cscope.out")
			endif
			if(csoutdeleted!=0)
				echohl WarningMsg | echo "Fail to do cscope! I cannot delete the cscope.out" | echohl None
				return
			endif
		endif
		if(executable('ctags'))
			"silent! execute "!ctags -R --c-types=+p --fields=+S *"
			silent! execute "!ctags -R --c++-kinds=+p --fields=+iaS --extra=+q ."
		endif
		if(executable('cscope') && has("cscope") )
			if(g:iswindows!=1)
				silent! execute "!find . -name '*.h' -o -name '*.c' -o -name '*.cpp' -o -name '*.java' -o -name '*.cs' > cscope.files"
			else
				silent! execute "!dir /s/b *.c,*.cpp,*.h,*.java,*.cs >> cscope.files"
			endif
			silent! execute "!cscope -b"
			execute "normal :"
			if filereadable("cscope.out")
				execute "cs add cscope.out"
			endif
		endif
	endfunction
	
#vim
