## 快捷键：
快捷键               | 模式                   | 备注
-------------------- | --------------------   |  ------------------
shift + 3            | 正常模式               | 快速搜索光标所在位置单词
tabnew file          | 命令模式               | 打开指定文件的标签(gt切换)
vsp                  | 命令模式               | 分页
set mouse=a          | 命令模式               | 允许鼠标操作
set ts=4             | 命令模式               | 设置tab为4个空格
set expandtab        | 命令模式               | 设置为真实的4个空格
set shiftwidth=4     | 命令模式               | 设置`>G`为4个空格
set nu               | 命令模式               | 显示行号
set hls              | 命令模式               | 查找高亮显示


## 插件管理
[Vundle](https://github.com/VundleVim/Vundle.vim)（Vim bundle）是一个Vim的插件管理器。它是把git操作整合进去，用户需要做的只是去GitHub上找到自己想要的插件的名字，安装、更新和卸载都可有vundle来完成了。插件主要分为两部分，添加插件与配置插件!


1. 添加插件: 在`.vimrc`配置文件中添加`Bundle 'Valloric/YouCompleteMe'`
2. 配置配置: 编写`.vimrc`,各插件配置参考官方文档


###  自动缩进：
1. `Plugin 'vim-scripts/indentpython.vim'`


### 代码补全:
1. `Bundle 'Valloric/YouCompleteMe'`

### 快速执行:
1. `Bundle 'thinca/vim-quickrun'`
2. vimrc 配置:


```vim
let g:quickrun_config = {
\   "_" : {
\       "outputter" : "message",
\   },
\}
let g:quickrun_no_default_key_mappings = 1
nmap <Leader>r <Plug>(quickrun)
map <F5> :QuickRun<CR>
```


### flake8规范检查:
1. `Bundle 'nvie/vim-flake8'`
2. .vimrc 配置:


```vim
autocmd FileType python map <buffer> <F4> :call Flake8()<CR>
```


### 语法检查:
1. `Bundle 'scrooloose/syntastic'`


### 树形目录:
1. `Plugin 'scrooloose/nerdtree'`
2. .vimrc 配置:


```vim
:map <F2> <ESC>:NERDTree %<CR>
nnoremap <F2> :exe 'NERDTreeToggle'<CR>
```


### 树形目录增强:
1. `Plugin 'jistr/vim-nerdtree-tabs'`


### powerline:
1. `Bundle 'Lokaltog/vim-powerline'`


### 行尾多余空格标红:
1. `Bundle 'bronson/vim-trailing-whitespace'`


### 大纲式导航:


1. `Bundle 'majutsushi/tagbar'`
2. .vimrc 配置:


```vim
autocmd VimEnter * TagbarToggle
nmap <F3> :TagbarToggle<CR>
```

