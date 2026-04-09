/** 
 *  @author TalkTao
 * @description  按需引入Vant
*/ 
import { Button, Tabbar, TabbarItem, Sticky, NavBar, Icon, Search, DropdownMenu, DropdownItem, Image, Lazyload, Tabs, Tab, Toast, Field, Cell, CellGroup, Form, List, Tag, Uploader, Progress, Empty, PullRefresh, Popup, Swipe, SwipeItem, Dialog, Loading } from 'vant'
const pluginsVant = [
	Button, 
	Tabbar,
	TabbarItem,
	Sticky,
	NavBar,
	Icon,
	Search,
	DropdownMenu,
	DropdownItem,
	Image,
	Lazyload,
	Tabs,
	Tab,
	Toast,
	Field,
	Cell,
	CellGroup,
	Form,
	List,
	Tag,
	Uploader,
	Progress,
	Empty,
	PullRefresh,
	Popup,
	Swipe,
	SwipeItem,
	Dialog,
	Loading
]
export const vantPlugins = {
  	install: function(vm) {
    	pluginsVant.forEach((item:any) => {
      	vm.component(item.name, item);
    	});
  	}
};