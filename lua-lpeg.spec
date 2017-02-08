%global luaver 5.3
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}
%define debug_package %nil

Name:           lua-lpeg
Version:	1.0.1
Release:        1
Summary:        Parsing Expression Grammars for Lua

Group:          Development/Other
License:        MIT
URL:            http://www.inf.puc-rio.br/~roberto/lpeg/
Source0:        http://www.inf.puc-rio.br/~roberto/lpeg/lpeg-%{version}.tar.gz

BuildRequires:  lua-devel >= %{luaver}
Requires:       lua >= %{luaver}

%description
LPeg is a new pattern-matching library for Lua, based on Parsing Expression
Grammars (PEGs).

%prep
%setup -q -n lpeg-%{version}
%{__sed} -i -e "s|/usr/bin/env lua5.1|%{_bindir}/lua|" test.lua
# strict module not part of our Lua 5.1.4
%{__sed} -i -e 's|require"strict"|-- require"strict"|' test.lua
%{__chmod} -x test.lua

%build
%make COPT="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{lualibdir}
%{__mkdir_p} %{buildroot}%{luapkgdir}
%{__install} -p lpeg.so %{buildroot}%{lualibdir}/lpeg.so.%{version}
%{__ln_s} lpeg.so.%{version} %{buildroot}%{lualibdir}/lpeg.so
%{__install} -p -m 0644 re.lua %{buildroot}%{luapkgdir}


%check
#lua test.lua

%files
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%{lualibdir}/*
%{luapkgdir}/*
