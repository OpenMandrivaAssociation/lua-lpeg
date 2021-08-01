%global luaver %(lua -e 'print(_VERSION)' | cut -d ' ' -f 2)
%global luajitver 2.1
%global luajitlver %(luajit -e 'print(_VERSION)' | cut -d ' ' -f 2)
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}
%global luajitlibdir %{_libdir}/lua/%{luajitlver}
%global luajitpkgdir %{_datadir}/lua/%{luajitlver}

Name:           lua-lpeg
Version:	1.0.2
Release:        1
Summary:        Parsing Expression Grammars for Lua

Group:          Development/Other
License:        MIT
URL:            http://www.inf.puc-rio.br/~roberto/lpeg/
Source0:        http://www.inf.puc-rio.br/~roberto/lpeg/lpeg-%{version}.tar.gz

BuildRequires:  lua-devel
BuildRequires:	lua
Requires:       lua

BuildRequires:	pkgconfig(luajit)
BuildRequires:	luajit

%description
LPeg is a new pattern-matching library for Lua, based on Parsing Expression
Grammars (PEGs).

%package -n luajit-lpeg
Summary:	Parsing Expression Grammars for Luajit

%description -n luajit-lpeg
LPeg is a new pattern-matching library for Luajit, based on Parsing Expression
Grammars (PEGs).

%prep
%autosetup -p1 -n lpeg-%{version}
%{__sed} -i -e "s|/usr/bin/env lua5.1|%{_bindir}/lua|" test.lua
# strict module not part of our Lua 5.1.4
%{__sed} -i -e 's|require"strict"|-- require"strict"|' test.lua
%{__chmod} -x test.lua

%build
%make_build COPT="%{optflags} -DNDEBUG"

mv lpeg.so lpeg.so.lua

%make_build clean
%make_build COPT="%{optflags} -DNDEBUG -I%{_includedir}/luajit-2.1"


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{lualibdir}
%{__mkdir_p} %{buildroot}%{luapkgdir}
%{__install} -p lpeg.so.lua %{buildroot}%{lualibdir}/lpeg.so
%{__install} -p -m 0644 re.lua %{buildroot}%{luapkgdir}

%{__mkdir_p} %{buildroot}%{luajitlibdir}
%{__mkdir_p} %{buildroot}%{luajitpkgdir}
%{__install} -p lpeg.so %{buildroot}%{luajitlibdir}/lpeg.so
%{__install} -p -m 0644 re.lua %{buildroot}%{luajitpkgdir}


#%check
#lua test.lua

%files
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%{lualibdir}/*
%{luapkgdir}/*

%files -n luajit-lpeg
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%{luajitlibdir}/*
%{luajitpkgdir}/*
